import pickle
from batteryabn import logger, Constants as Const
from batteryabn.models import Cell, Project
from batteryabn.repositories import CellRepository, TestRecordRepository, ProjectRepository
from batteryabn.utils import Processor, Viewer, Utils


class CellService:
    """
    The CellService class provides an interface for creating and querying Cell objects.
    """
    def __init__(self, cell_repository: CellRepository, test_record_repository: TestRecordRepository, project_repository: ProjectRepository):
        self.cell_repository = cell_repository
        self.test_record_repository = test_record_repository
        self.project_repository = project_repository


    def create_cell(self, cell_name: str):
        """
        This method creates a new Cell instance and adds it to the session.

        Parameters
        ----------
        cell_name : str
            The unique name of the cell.

        Returns
        -------
        Cell
            The newly created Cell object
        """
        cell = self.cell_repository.find_by_name(cell_name)
        if cell:
            logger.info(f'Found existing cell: {cell_name}')
            return cell

        cell = Cell(cell_name=cell_name.upper())  # Assuming cell names are case-insensitive and stored as uppercase
        self.cell_repository.add(cell)
        try:
            self.cell_repository.commit()
            logger.info(f'Created new cell: {cell_name}')
        except Exception as e:
            self.cell_repository.rollback()
            logger.error(f'Failed to create new cell: {cell_name}. Error: {e}')
            raise

        return cell
    
    def process_cell(self, cell_name: str, processor: Processor, viewer: Viewer):
        """
        Process cell data and save it to the database.

        Parameters
        ----------
        cell : Cell
            The cell to process
        processor : Processor
            Processor object with processed cell data
        """
        cell = self.find_cell_by_name(cell_name)

        if not cell:
            logger.error(f'Cell not found: {cell_name}')
            return
        
        cycler_trs, vdf_trs = self.get_cycler_vdf_trs(cell)
        # Process cell data
        processor.process(cycler_trs, vdf_trs, cell.project)
        # Genrate images for processed data
        img_cell, img_ccm, img_ccm_aht = viewer.plot(processor, cell.cell_name)

        # Update cell data
        cell.cell_data = Utils.gzip_pikle_dump(processor.cell_data)
        cell.cell_cycle_metrics = Utils.gzip_pikle_dump(processor.cell_cycle_metrics)
        cell.cell_data_vdf = Utils.gzip_pikle_dump(processor.cell_data_vdf)

        cell.image_cell = Utils.image_to_binary(img_cell)
        cell.image_ccm = Utils.image_to_binary(img_ccm)
        cell.image_ccm_aht = Utils.image_to_binary(img_ccm_aht)

        # Save cell data
        try:
            self.cell_repository.commit()
            logger.info(f'Processed and saved data for cell: {cell_name}')
        except Exception as e:
            self.cell_repository.rollback()
            logger.error(f'Failed to save processed data for cell: {cell_name}. Error: {e}')
            raise e
        
    def load_cell_images(self, cell_name: str):
        """
        Load cell images from the database.

        Parameters
        ----------
        cell_name : str
            The unique name of the cell.

        Returns
        -------
        tuple
            The images for the cell
        """
        cell = self.find_cell_by_name(cell_name)

        if not cell:
            logger.error(f'Cell not found: {cell_name}')
            return
        
        return cell.load_image_cell(), cell.load_image_ccm(), cell.load_image_ccm_aht()

    def get_combined_cell_data(self, cell_name: str, processor: Processor):
        """
        Get combined cell cycler and vdf data for a cell.

        Parameters
        ----------
        cell_name : str
            The unique name of the cell.
        processor : Processor
            Processor object with processed cell data

        Returns
        -------
        dict
            Combined cell data
        """
        cell = self.find_cell_by_name(cell_name)

        if not cell:
            logger.error(f'Cell not found: {cell_name}')
            return
        
        cycler_trs, vdf_trs = self.get_cycler_vdf_trs(cell)
        # Process cell data
        return processor.combine_data(cycler_trs, vdf_trs)


    def change_cell_project(self, cell_name: str, new_project_name: str):
        """
        Change the project associated with a cell to a new project.

        Parameters
        ----------
        cell_name : str
            The unique name of the cell.
        new_project_name : str
            The name of the new project to associate with the cell.
        """
        # Find the cell by name
        cell = self.cell_repository.find_by_name(cell_name)
        if not cell:
            logger.error(f'Cell with name {cell_name} not found.')
            return

        # Find or create the new project
        project = self.project_repository.find_by_name(new_project_name)
        if not project:
            logger.info(f'Creating new project: {new_project_name}')
            project = Project(project_name=new_project_name)
            self.project_repository.add(project)

        # Associate the cell with the new project
        cell.project = project
        logger.info(f'Cell {cell_name} is now associated with project {new_project_name}.')

        # Commit the changes
        try:
            self.cell_repository.commit()
            logger.info(f'Successfully updated project association for cell: {cell_name}.')
        except Exception as e:
            self.cell_repository.rollback()
            logger.error(f'Failed to update project association for cell: {cell_name}. Error: {e}')
            raise


    def get_cycler_vdf_trs(self, cell: Cell):
        """
        Get cycler and Vdf test records for a cell.

        Parameters
        ----------
        cell : Cell
            The cell to get test records for

        Returns
        -------
        list
            Cycler test records
        list
            Vdf test records
        """
        trs = self.test_record_repository.find_by_cell_name(cell.cell_name)
        cycler_trs, vdf_trs = [], []
        for tr in trs:
            if tr.test_type == Const.VDF:
                vdf_trs.append(tr)
            else:
                cycler_trs.append(tr)
        return cycler_trs, vdf_trs

    def find_cell_by_name(self, cell_name: str):
        """
        This method finds a Cell by its name.

        Parameters
        ----------
        cell_name : str
            The name of the cell to find

        Returns
        -------
        Cell
            The Cell object with the specified name
        """
        return self.cell_repository.find_by_name(cell_name)
    
    def find_cells_by_project_name(self, project_name: str):
        """
        This method finds all Cells in a Project.

        Parameters
        ----------
        project_name : str
            The name of the project to find cells for

        Returns
        -------
        list
            A list of Cell objects in the specified project
        """
        return self.cell_repository.find_by_project(project_name)
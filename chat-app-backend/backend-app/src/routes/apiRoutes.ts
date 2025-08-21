import { Router } from 'express';
import { QueryController } from '../controllers/queryController';
import { Express } from 'express';

const router = Router();
const queryController = new QueryController();

export const setApiRoutes = (app: Express) => {
    app.use('/api', router);

    router.post('/query', queryController.handleQuery.bind(queryController));
};

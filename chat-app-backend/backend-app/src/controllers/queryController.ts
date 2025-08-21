import { Request, Response } from 'express';
import { sendQueryToOllama } from '../api/ollama';
import { logError, handleResponse, handleErrorResponse } from '../utils/index';

export class QueryController {
    public async handleQuery(req: Request, res: Response): Promise<void> {
        const query = req.body.query;

        if (!query) {
            handleErrorResponse(res, new Error('Query is required'), 400);
            return;
        }

        try {
            const response = await sendQueryToOllama(query);
            handleResponse(res, { response });
        } catch (error) {
            handleErrorResponse(res, error as Error);
        }
    }
}

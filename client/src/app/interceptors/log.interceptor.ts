import { HttpHandlerFn, HttpInterceptorFn, HttpRequest } from '@angular/common/http';

export const logInterceptor: HttpInterceptorFn = (req: HttpRequest<unknown>, next: HttpHandlerFn) => {
  console.log("Request for " + req.method + " " + req.url);
  console.log("Headers: ", req.headers);
  return next(req);
};

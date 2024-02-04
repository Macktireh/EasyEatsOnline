import { HttpClient } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';

import { environment } from '../../environments/environment.development';
import { LoginModels, SignupModels } from '@/models/auth.models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private baseUrl = environment.baseUrl;

  private readonly httpClient = inject(HttpClient);

  public login(model: LoginModels) {
    return this.httpClient.post(`${this.baseUrl}/auth/login`, model.toJson())
  }

  public signup(payload: SignupModels) {
    return this.httpClient.post(`${this.baseUrl}/auth/signup`, payload.toJson())
  }
  
}

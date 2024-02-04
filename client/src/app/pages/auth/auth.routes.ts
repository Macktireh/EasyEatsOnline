import { Routes } from "@angular/router";


export const routes: Routes = [
  {
    path: 'login',
    title: 'Login - Easy Eats',
    loadComponent: () => import('./login/login.component').then((m) => m.LoginComponent)
  },
  {
    path: 'signup',
    title: 'Signup - Easy Eats',
    loadComponent: () => import('./signup/signup.component').then((m) => m.SignupComponent)
  },
  {
    path: '',
    redirectTo: '/auth/login',
    pathMatch: 'full'
  }
] 

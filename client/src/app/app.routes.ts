import { Routes } from '@angular/router';

import { HomeComponent } from '@/pages/home/home.component';

export const routes: Routes = [
  {
    path: '',
    title: 'Home - Easy Eats',
    component: HomeComponent
  },
  {
    path: 'auth',
    loadChildren: () => import('./pages/auth/auth.routes').then((m) => m.routes)
  }
];

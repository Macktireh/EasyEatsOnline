import { HttpClient } from '@angular/common/http';
import { Component, inject } from '@angular/core';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [],
  templateUrl: './login.component.html',
})
export class LoginComponent {
  private readonly httpClient = inject(HttpClient);

  ngOnInit() {
    this.httpClient
      .get('https://jsonplaceholder.typicode.com/todos/2')
      .subscribe((data) => console.log(data));
  }
}

import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, inject } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [HttpClientModule],
  templateUrl: './home.component.html',
})
export class HomeComponent {
  private readonly httpClient = inject(HttpClient);

  ngOnInit() {
    this.httpClient
      .get('https://jsonplaceholder.typicode.com/todos/1')
      .subscribe((data) => console.log(data));
  }
}

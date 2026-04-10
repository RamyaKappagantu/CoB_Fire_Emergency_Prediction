import { Component , ChangeDetectorRef} from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth/auth.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Front-end-App';
  isLoggedIn = false;

  constructor(public authService: AuthService, private router: Router,private cdr: ChangeDetectorRef) { 
  }

  ngOnInit() {
    this.authService.isLoggedIn.subscribe(loggedIn => {
      this.isLoggedIn = loggedIn;
      if (loggedIn) {
        this.router.navigate(['home']);
      } else {
        this.router.navigate(['/login']);
      }
      this.cdr.detectChanges(); // Manually trigger change detection
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
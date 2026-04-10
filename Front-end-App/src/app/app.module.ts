import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { LSTMResultComponent } from './views/lstm-result/lstm-result.component';
import { ProphetResultComponent } from './views/prophet-result/prophet-result.component';
import { VARResultComponent } from './views/var-result/var-result.component';
import { LstmPredictionService } from './services/LSTM-prediction/lstm-prediction.service';
import { VARPredictionService } from './services/VAR-prediction/VAR-prediction.service';
import { MapViewComponent } from './views/map-view/map-view.component';
import { CoordinatesService } from './services/Coordinates-service/coordinates.service';
import { JwtModule, JWT_OPTIONS } from '@auth0/angular-jwt';
import { AuthService } from './services/auth/auth.service';
import { RegisterComponent } from './views/register/register.component';
import { LoginComponent } from './views/login/login.component';
import { FormsModule } from '@angular/forms';
import { HomeComponent } from './views/home/home.component';
import { AppComponent } from './app.component';
import { DatePickerComponent } from './views/date-picker/date-picker/date-picker.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatNativeDateModule } from '@angular/material/core';
import { MatIconModule } from '@angular/material/icon';
import { MAT_SNACK_BAR_DEFAULT_OPTIONS, MatSnackBarModule } from '@angular/material/snack-bar';

export function jwtOptionsFactory() {
  return {
    tokenGetter: () => {
      return localStorage.getItem('access_token');
    },
    allowedDomains: ['127.0.0.1:5000'],
    disallowedRoutes: ['http://127.0.0.1:5000/auth/login']
  };
}

@NgModule({
  declarations: [
    AppComponent,
    LSTMResultComponent,
    ProphetResultComponent,
    VARResultComponent,
    MapViewComponent,
    LoginComponent,
    RegisterComponent,
    HomeComponent,
    DatePickerComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    MatDatepickerModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatNativeDateModule,
    MatIconModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSnackBarModule,
    HttpClientModule,
    FormsModule,
    JwtModule.forRoot({
      jwtOptionsProvider: {
        provide: JWT_OPTIONS,
        useFactory: jwtOptionsFactory
      }
    })
  ],
  providers: [
    LstmPredictionService, VARPredictionService, CoordinatesService,AuthService,
    { 
      provide: MAT_SNACK_BAR_DEFAULT_OPTIONS, 
      useValue: { 
        duration: 100000,  // Set duration to 5 seconds or any desired duration
        horizontalPosition: 'center',
        verticalPosition: 'top'
      } 
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

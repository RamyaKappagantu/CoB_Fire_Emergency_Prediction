import { TestBed } from '@angular/core/testing';

import { VARPredictionService } from './VAR-prediction.service';

describe('VARPredictionService', () => {
  let service: VARPredictionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VARPredictionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

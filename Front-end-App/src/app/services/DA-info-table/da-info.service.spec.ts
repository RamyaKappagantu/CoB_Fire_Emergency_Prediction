import { TestBed } from '@angular/core/testing';

import { DAInfoService } from './da-info.service';

describe('DAInfoService', () => {
  let service: DAInfoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DAInfoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});

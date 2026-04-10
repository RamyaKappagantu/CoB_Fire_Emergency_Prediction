import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VARResultComponent } from './var-result.component';

describe('VARResultComponent', () => {
  let component: VARResultComponent;
  let fixture: ComponentFixture<VARResultComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [VARResultComponent]
    });
    fixture = TestBed.createComponent(VARResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

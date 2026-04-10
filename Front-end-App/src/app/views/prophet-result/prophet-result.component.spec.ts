import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProphetResultComponent } from './prophet-result.component';

describe('ProphetResultComponent', () => {
  let component: ProphetResultComponent;
  let fixture: ComponentFixture<ProphetResultComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ProphetResultComponent]
    });
    fixture = TestBed.createComponent(ProphetResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

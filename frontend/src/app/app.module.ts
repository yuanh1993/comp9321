import { BrowserModule } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TestComponent } from './test/test.component';
import { NavbarComponent } from './navbar/navbar.component';
import { HttpClientModule }    from '@angular/common/http';
import { ShowgraphComponent } from './showgraph/showgraph.component';
import { RankComponent } from './rank/rank.component';
import { ClusteringComponent } from './clustering/clustering.component';
import { PredictionComponent, NgbdModalContent} from './prediction/prediction.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatRadioModule } from '@angular/material/radio';
import { MatNativeDateModule } from '@angular/material';

@NgModule({
  declarations: [
    AppComponent,
    TestComponent,
    NavbarComponent,
    ShowgraphComponent,
    RankComponent,
    ClusteringComponent,
    PredictionComponent,
    NgbdModalContent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NgbModule,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatButtonToggleModule,
    MatRadioModule,
    MatNativeDateModule,
  ],
  providers: [],
  entryComponents: [NgbdModalContent],
  bootstrap: [AppComponent]
})
export class AppModule { }

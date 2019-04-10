import { NgModule } from '@angular/core';
import {TestComponent} from './test/test.component';
import { Routes, RouterModule } from '@angular/router';
import { ShowgraphComponent } from './showgraph/showgraph.component';
import { RankComponent } from './rank/rank.component';
import { ClusteringComponent } from './clustering/clustering.component';
import { PredictionComponent } from './prediction/prediction.component';

const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: TestComponent },
  { path: 'showgraph', component: ShowgraphComponent },
  { path: 'rank', component: RankComponent },
  { path: 'prediction', component: PredictionComponent },
  { path: 'clustering', component: ClusteringComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

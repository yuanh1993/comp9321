import { NgModule } from '@angular/core';
import {TestComponent} from './test/test.component';
import { Routes, RouterModule } from '@angular/router';
import {ShowgraphComponent} from './showgraph/showgraph.component';


const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: 'home', component: TestComponent },
  { path: 'showgraph', component: ShowgraphComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

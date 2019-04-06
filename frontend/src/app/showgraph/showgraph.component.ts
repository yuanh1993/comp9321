import { Component, OnInit } from '@angular/core';
import {GetdataService} from '../getdata.service';
@Component({
  selector: 'app-showgraph',
  templateUrl: './showgraph.component.html',
  styleUrls: ['./showgraph.component.css']
})
export class ShowgraphComponent implements OnInit {
  d:object;
  constructor(
    private getdataservice:GetdataService,

  ) { }

  ngOnInit() {
    this.getdataservice.getdata(5).subscribe(
    data=>{
      console.log(data);
      this.d=data;
    });
  }

}

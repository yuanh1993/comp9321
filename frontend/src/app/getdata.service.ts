import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({
    'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
    'Access-Control-Allow-Methods': 'GET,PUT,POST,DELETE,PATCH,OPTIONS',
    'Access-Control-Allow-Headers': 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token',
  }),
  withCredentials: true,
  //observe: 'response',
}

@Injectable({
  providedIn: 'root'

})
export class GetdataService {
  baseurl="http://127.0.0.1:5000/api"
  constructor(
  private http: HttpClient,
  ) {}
  getdata(id:number){
    return this.http.get<any>(`${this.baseurl}/getData/${id}`);
  }


}

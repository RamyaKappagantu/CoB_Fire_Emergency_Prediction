// src/typings/shpjs.d.ts
declare module 'shpjs' {
    const shp: {
      (input: string | ArrayBuffer | Blob): Promise<any>;
    };
    export default shp;
  }
  
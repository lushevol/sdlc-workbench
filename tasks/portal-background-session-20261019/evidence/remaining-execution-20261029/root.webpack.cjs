const path = require('path');
const repo = "/var/folders/3q/zc3tlwsj1p1_pskzk1j9r5100000gn/T/comprehensive-renewal-c4g7zsd3/root-source";
const sourceConfig = require(path.join(repo, 'webpack.config.js'));
module.exports=(env,argv)=>{
 const config=sourceConfig(env,argv);
 config.output.path=path.join(__dirname,'build');
 config.devServer={...config.devServer,host:'127.0.0.1',port:8343,allowedHosts:['localhost','127.0.0.1'],open:false,hot:false,liveReload:false,client:false,static:{directory:path.join(repo,'public')},proxy:[{context:['/api/'],target:'http://127.0.0.1:8291',changeOrigin:true}],setupMiddlewares(middlewares,server){
 server.app.get('/importmaplocal.json',(_req,res)=>{const map=require(path.join(repo,'public/importmaplocal.json'));res.json({...map,imports:{...map.imports,'@fm/base':'http://127.0.0.1:8342/base.js'}});});
 return middlewares;
 }};
 return config;
};

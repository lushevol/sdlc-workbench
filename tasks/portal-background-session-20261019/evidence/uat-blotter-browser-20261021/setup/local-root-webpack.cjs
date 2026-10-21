const path = require('path');
const repo = "/Users/lushevol/code/github/ratan-release-impact/workbench/repos/ui/mfe-root-config";
const sourceConfig = require(path.join(repo, 'webpack.config.js'));
module.exports=(env,argv)=>{
 const config=sourceConfig(env,argv);
 config.output.path=path.join(__dirname,'build');
 config.devServer={...config.devServer,host:'127.0.0.1',port:8121,allowedHosts:['localhost','127.0.0.1'],open:false,hot:false,liveReload:false,client:false,static:{directory:path.join(repo,'public')},proxy:[{context:['/api/'],target:'http://127.0.0.1:8123',changeOrigin:true}],setupMiddlewares(middlewares,server){
 server.app.get('/importmaplocal.json',(_req,res)=>{const map=require(path.join(repo,'public/importmaplocal.json'));res.json({...map,imports:{...map.imports,'@fm/base':'http://127.0.0.1:8122/base.js','@fm/ratan_container':'http://127.0.0.1:8125/ratan_container.js','@fm/ratan_cashflow_blotter':'http://127.0.0.1:8124/ratan_cashflow_blotter.js'}});});
 return middlewares;
 }};
 return config;
};

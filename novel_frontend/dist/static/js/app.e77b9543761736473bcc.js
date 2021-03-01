webpackJsonp([1],{"73K0":function(t,e){},NHnr:function(t,e,i){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var o=i("7+uW"),r={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"app"}},[e("img",{attrs:{src:i("hAgk")}}),this._v(" "),e("router-view")],1)},staticRenderFns:[]};var l=i("VU/8")({name:"App"},r,!1,function(t){i("rNfs")},null,null).exports,a=i("/ocq"),n=i("mtWM"),s=i.n(n),c={name:"NovelAnalysis",data:function(){return{msg:"小说漫画分析平台",form:{word2vec_file:"",source_path:"",source_file:"",target_path:"",target_file:""},pic:"",init_loading:!1,analysis_loading:!1,logArr:["欢迎使用小说漫画分析平台"],number:0}},computed:{log:function(){return{id:this.number,val:this.logArr[this.number]}}},methods:{initModel:function(){var t=this;this.init_loading=!0,this.number+=1,this.logArr.push("开始初始化模型"),console.log("开始初始化模型");var e={word2vec_file:this.form.word2vec_file};s.a.post("/init",e).then(function(e){t.number+=1,t.logArr.push("小说分析模型初始化完成"),console.log("模型初始化完成"),t.loadingFalse()}).catch(function(e){t.number+=1,t.logArr.push("模型初始化失败"),console.log("模型初始化失败"),t.loadingFalse()})},startAnalysis:function(){var t=this;this.analysis_loading=!0;var e={source_path:this.form.source_path,source_file:this.form.source_file,target_path:this.form.target_path,target_file:this.form.target_file};s.a.post("/analysis",e).then(function(e){t.pic=e.data,t.number+=1,t.logArr.push("小说文本分析完成！"),console.log("小说分析完成"),setTimeout(function(){t.number+=1,t.logArr.push("分析结果保存在`"+t.form.target_path+"`中的`"+t.form.target_file+"`文件中"),console.log("显示保存文件的路径")},2e3),t.loadingFalse()}).catch(function(e){t.number+=1,t.logArr.push("小说分析失败，具体错误请查看日志！"),console.log("小说分析失败"),t.loadingFalse()})},downloadPic:function(){this.number+=1,this.logArr.push("下载词云图片");var t="data:image/png;base64,"+this.pic,e=document.createElement("a");e.href=t,e.setAttribute("download","word-cloud"),e.click()},loadingFalse:function(){this.init_loading=!1,this.analysis_loading=!1}},watch:{init_loading:function(t){console.log("观测到了init_loading的变化"),t&&(this.number+=1,this.logArr.push("开始初始化模型"),console.log("开始初始化模型"))},analysis_loading:function(t){console.log("观测到了analysis_loading的变化"),t&&(this.number+=1,this.logArr.push("对小说文本"+this.form.source_file+"进行分析"),console.log("开始分析小说"))}}},d={render:function(){var t=this,e=t.$createElement,i=t._self._c||e;return i("div",[i("h1",[t._v(t._s(t.msg))]),t._v(" "),i("el-divider"),t._v(" "),i("div",{attrs:{id:"input-form"}},[i("el-form",{ref:"form",attrs:{model:t.form,"label-position":"top"}},[i("el-form-item",{attrs:{label:"词向量文件路径",required:""}},[i("el-input",{staticStyle:{width:"800px"},attrs:{placeholder:"请输入词向量文件路径","prefix-icon":"el-icon-document-copy",clearable:""},model:{value:t.form.word2vec_file,callback:function(e){t.$set(t.form,"word2vec_file",e)},expression:"form.word2vec_file"}})],1),t._v(" "),i("el-divider"),t._v(" "),i("el-form-item",{attrs:{label:"大纲文件目录和文件名",required:""}},[i("el-input",{staticStyle:{width:"400px"},attrs:{placeholder:"文件目录","prefix-icon":"el-icon-folder-opened"},model:{value:t.form.source_path,callback:function(e){t.$set(t.form,"source_path",e)},expression:"form.source_path"}}),t._v(" "),i("el-input",{staticStyle:{width:"400px"},attrs:{placeholder:"文件名","prefix-icon":"el-icon-document"},model:{value:t.form.source_file,callback:function(e){t.$set(t.form,"source_file",e)},expression:"form.source_file"}})],1),t._v(" "),i("el-divider"),t._v(" "),i("el-form-item",{attrs:{label:"保存到文件目录和文件名：",required:""}},[i("el-input",{staticStyle:{width:"400px"},attrs:{placeholder:"文件目录","prefix-icon":"el-icon-folder-opened"},model:{value:t.form.target_path,callback:function(e){t.$set(t.form,"target_path",e)},expression:"form.target_path"}}),t._v(" "),i("el-input",{staticStyle:{width:"400px"},attrs:{placeholder:"文件名","prefix-icon":"el-icon-document"},model:{value:t.form.target_file,callback:function(e){t.$set(t.form,"target_file",e)},expression:"form.target_file"}})],1)],1)],1),t._v(" "),i("div",{attrs:{id:"word-img"}},[i("el-image",{attrs:{src:"data:image/png;base64,"+t.pic,fit:"fill"}},[i("div",{staticClass:"image-slot",attrs:{slot:"error"},slot:"error"},[i("i",{staticClass:"el-icon-picture-outline"})])])],1),t._v(" "),i("div",{attrs:{id:"operation"}},[i("el-row",[i("el-button",{attrs:{type:"primary",loading:t.init_loading,round:""},on:{click:t.initModel}},[t._v("初始化模型")]),t._v(" "),i("el-button",{attrs:{type:"success",loading:t.analysis_loading},on:{click:t.startAnalysis}},[t._v("小说分析")]),t._v(" "),i("el-button",{attrs:{type:"danger"},on:{click:t.downloadPic}},[t._v("下载词云")])],1)],1),t._v(" "),i("el-divider"),t._v(" "),i("el-divider",[i("span",[t._v("输出日志")])]),t._v(" "),i("div",{staticClass:"transition-box"},[i("transition",{attrs:{name:"slide"}},[i("p",{key:t.log.id,staticClass:"log"},[t._v(t._s(t.log.val))])])],1),t._v(" "),i("el-divider")],1)},staticRenderFns:[]};var u=i("VU/8")(c,d,!1,function(t){i("73K0")},"data-v-5406f77a",null).exports;o.default.use(a.a);var f=new a.a({routes:[{path:"/",name:"NovelAnalysis",component:u}]}),p=i("zL8q"),m=i.n(p);i("tvR6");o.default.config.productionTip=!1,o.default.use(m.a),o.default.prototype.axios=s.a,new o.default({el:"#app",router:f,components:{App:l},template:"<App/>"})},hAgk:function(t,e,i){t.exports=i.p+"static/img/platform.eb22d0d.png"},rNfs:function(t,e){},tvR6:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.e77b9543761736473bcc.js.map
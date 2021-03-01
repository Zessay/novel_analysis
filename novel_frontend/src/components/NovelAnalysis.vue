<template>
  <div>
    <h1>{{ msg }}</h1>
    <el-divider></el-divider>
    <div id="input-form">
    <el-form ref="form" :model="form" label-position="top">
      <el-form-item label="词向量文件路径" required>
        <el-input placeholder="请输入词向量文件路径" prefix-icon="el-icon-document-copy" style="width:800px;" v-model="form.word2vec_file" clearable>
        </el-input>
      </el-form-item>
      <el-divider></el-divider>
      <el-form-item label="大纲文件目录和文件名" required>
        <el-input placeholder="文件目录"  prefix-icon="el-icon-folder-opened" style="width:400px;" v-model="form.source_path"></el-input>
        <el-input placeholder="文件名" prefix-icon="el-icon-document" style="width:400px;" v-model="form.source_file"></el-input>
      </el-form-item>
      <el-divider></el-divider>
      <el-form-item label="保存到文件目录和文件名：" required>
        <el-input placeholder="文件目录"  prefix-icon="el-icon-folder-opened" style="width:400px;" v-model="form.target_path"></el-input>
        <el-input placeholder="文件名" prefix-icon="el-icon-document" style="width:400px;" v-model="form.target_file"></el-input>
      </el-form-item>
    </el-form>
    </div>
    <div id="word-img">
      <el-image :src="'data:image/png;base64,'+pic" fit="fill">
          <div slot="error" class="image-slot">
              <i class="el-icon-picture-outline"></i>
          </div>
      </el-image>
    </div>
    <div id="operation">
      <el-row>
          <el-button type="primary" :loading="init_loading" @click="initModel" round>初始化模型</el-button>
          <el-button type="success" :loading="analysis_loading" @click="startAnalysis">小说分析</el-button>
          <el-button type="danger"  @click="downloadPic">下载词云</el-button>
      </el-row>
    </div>
    <!-- 输出日志 -->
    <el-divider></el-divider>
    <el-divider><span>输出日志</span></el-divider>
    <div class="transition-box">
      <transition name="slide">
        <p class="log" :key="log.id">{{log.val}}</p>
      </transition>
    </div>
    <el-divider></el-divider>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'NovelAnalysis',
  data () {
    return {
      msg: '小说漫画分析平台',
      form: {
        word2vec_file: '',
        source_path: '',
        source_file: '',
        target_path: '',
        target_file: ''
      },
      pic: '', // 词云图片
      init_loading: false,
      analysis_loading: false,
      // 用来保存日志的内容
      logArr: ['欢迎使用小说漫画分析平台'],
      // 表示当前需要显示日志的索引
      number: 0
    }
  },
  computed: {
    log () {
      return {
        id: this.number,
        val: this.logArr[this.number]
      }
    }
  },
  methods: {
    // 初始化模型函数
    initModel () {
      this.init_loading = true
      this.number += 1
      this.logArr.push('开始初始化模型')
      console.log('开始初始化模型')
      var param = {
        'word2vec_file': this.form.word2vec_file
      }
      axios.post('/init', param).then(
        res => {
          this.number += 1
          this.logArr.push('小说分析模型初始化完成')
          console.log('模型初始化完成')
          this.loadingFalse()
        }
      ).catch(res => {
        this.number += 1
        this.logArr.push('模型初始化失败')
        console.log('模型初始化失败')
        this.loadingFalse()
      })
    },
    // 开始对小说进行分析
    startAnalysis () {
      this.analysis_loading = true
      var param = {
        'source_path': this.form.source_path,
        'source_file': this.form.source_file,
        'target_path': this.form.target_path,
        'target_file': this.form.target_file
      }
      axios.post('/analysis', param).then(
        res => {
          this.pic = res.data // 词云图片
          this.number += 1
          this.logArr.push('小说文本分析完成！')
          console.log('小说分析完成')
          setTimeout(() => {
            this.number += 1
            this.logArr.push('分析结果保存在`' + this.form.target_path + '`中的`' + this.form.target_file + '`文件中')
            console.log('显示保存文件的路径')
          }, 2000)
          this.loadingFalse()
        }
      ).catch(res => {
        this.number += 1
        this.logArr.push('小说分析失败，具体错误请查看日志！')
        console.log('小说分析失败')
        this.loadingFalse()
      })
    },
    // 下载词云图片
    downloadPic () {
      this.number += 1
      this.logArr.push('下载词云图片')
      const imgUrl = 'data:image/png;base64,' + this.pic
      const a = document.createElement('a')
      a.href = imgUrl
      a.setAttribute('download', 'word-cloud')
      a.click()
    },
    loadingFalse () {
      this.init_loading = false
      this.analysis_loading = false
    }
  },
  watch: {
    // 观测是否处于初始化模型
    init_loading: function (value) {
      console.log('观测到了init_loading的变化')
      if (value) {
        this.number += 1
        this.logArr.push('开始初始化模型')
        console.log('开始初始化模型')
      }
    },
    // 观测处于分析状态的标志
    analysis_loading: function (value) {
      console.log('观测到了analysis_loading的变化')
      if (value) {
        this.number += 1
        this.logArr.push('对小说文本' + this.form.source_file + '进行分析')
        console.log('开始分析小说')
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
div {
  text-align: center;
  vertical-align: middle;
}
.slide-enter-active, .slide-leave-active {
  transition: all 0.5s linear;
}
.slide-enter{
  transform: translateY(20px) scale(1);
  opacity: 1;
}
.slide-leave-to {
  transform: translateY(-20px) scale(0.8);
  opacity: 0;
}
.transition-box {
  width: 400px;
  height: 100px;
  margin: 0 auto;
  /* margin-bottom: 10px; */
  border-radius: 4px;
  background-color: #e5e9f2;
  text-align: center;
  color: #e5e9f2;
  padding: 20px 20px;
  box-sizing: border-box;
  /* margin-right: 20px; */
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}
.log {
  width: 100%;
  height: 100px;
  margin: 0 auto;
  text-align: center;
  position: relative;
  font-family: "Hiragino Sans GB";
  color: #303133;
  font-size: 16px;
}
</style>

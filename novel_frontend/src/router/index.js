import Vue from 'vue'
import Router from 'vue-router'
import NovelAnalysis from '@/components/NovelAnalysis'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'NovelAnalysis',
      component: NovelAnalysis
    }
  ]
})

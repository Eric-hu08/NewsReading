import { createStore } from 'vuex'

export default createStore({
  state: {
    displayMode: 'vis',
    cNodeYArray: [],
    cNodeUnfoldArray: [],
    change_c_index:0,
    f_fold:0,   //1: unfold 2:fold
  },
  getters: {
    
  },
  mutations: {
    ['UPDATE_DISPLAY_MODE'] (state, displayMode) {
      state.displayMode = displayMode
    },
    
    editCNodeUnfoldArray(state,value){
      state.cNodeUnfoldArray[value]=1-state.cNodeUnfoldArray[value]
      console.log("foldarraychange!",state.cNodeUnfoldArray)
    },
    setCNodeUnfoldArray(state,value){
      state.cNodeUnfoldArray=value
    },
    setCNodeYArray(state,value){
      state.cNodeYArray=value
    },
    editCNodeYArray(state,{index,value}){
      var temp_array=lodash.cloneDeep(state.cNodeYArray)
      temp_array.splice(index,1,value)
      console.log("begin change cnnodea",temp_array,index,value)
      state.cNodeYArray=lodash.cloneDeep(temp_array)
      // var temp2=state.cNodeYArray.splice(index,1,value)
      // state.cNodeYArray.splice(index,1,value)
      // state.cNodeYArray=state.cNodeYArray.splice(index,1,value)
      // this.setCNodeYArray(temp_array.splice(index,1,value))
      // console.log("temp2",temp2,temp_array)
      // state.cNodeYArray=temp2
      
      console.log("cnodearray",state.cNodeYArray,value)
    },
    editChangeCIndex(state,value){
      state.change_c_index=value
    },
    editFFold(state,value){
      state.f_fold=value
    }
  },
    
  actions: {

  },
  modules: {

  }
})

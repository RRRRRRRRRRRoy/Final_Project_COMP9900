<template>
  <div style="width: 300px">
    <el-row justify="space-between" align="middel" style="height: 30px">
      <span>Address 1 </span></el-row
    >
    <address-input id="add_1" />
    <el-row
      ><span>{{ address.add_1 }}</span>
      <!-- <show-map /> -->
    </el-row>
  </div>
</template>


<script>
import addressInput from "./addressInput.vue";
import showMap from "./showMap.vue";
import { ref, reactive } from "vue";

export default {
  components: { addressInput, showMap },
  setup() {
    const address = reactive({
      1: "",
      2: "",
      3: "",
    });
    const showDialog = ref(false);
    const confirmEditAddr = () => {
      alert("close");
      showDialog.value = false;
    };
    return { address, showDialog, confirmEditAddr };
  },
};
</script>

<style scoped>
.el-drawer {
  z-index: -100;
}
</style>
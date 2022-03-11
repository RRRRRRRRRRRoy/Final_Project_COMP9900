<template>
  <div style="width: 100%">
    <el-card style="background-color: #788f77; border-radius: 10px">
      <div v-if="hPlan && !modifyMode">
        <el-row justify="center" style="height: 80vh"
          ><el-card style="border-radius: 10px" class="card"
            ><template #header
              ><el-row justify="space-between" style="height: 20px"
                ><span style="font-weight: bold; font-size: 25px"
                  >My Current Plan</span
                >
                <el-button @click="modifyPlan">Modify</el-button></el-row
              ></template
            ><plan-detail /></el-card
        ></el-row>
      </div>
      <div v-else><route-plan /></div>
    </el-card>
  </div>
</template>

<script>
import PlanDetail from "../components/planDetail.vue";
import routePlan from "../components/routePlan.vue";
import { onMounted, ref } from "vue";
export default {
  components: { routePlan, PlanDetail },
  data() {
    return {
      hPlan: this.havePlan(),
      modifyMode: false,
    };
  },

  methods: {
    modifyPlan() {
      this.modifyMode = true;
    },
    havePlan() {
      if (localStorage.getItem("plan") !== "null") {
        return true;
      } else {
        return false;
      }
    },
  },
};
</script>

<style scoped>
.card :deep(.el-card__body) {
  padding: 2px;
}
</style>
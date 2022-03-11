<template>
  <div class="not-login-container" v-if="!this.$root.logged">
    <el-row justify="center" align="middle" class="not-login">
      <el-card>
        <el-row> HOMEPAGE BUT YOU HAVE NOT LOGGED IN</el-row
        ><el-row> <el-link href="/login">login</el-link></el-row
        ><el-row> <el-link href="/register">register</el-link></el-row>
      </el-card>
    </el-row>
  </div>
  <div v-else>
    <el-card
      class="index-container"
      style="background-color: #788f77; border-radius: 10px"
    >
      <el-row justify="space-around" align="middle">
        <el-card
          style="
            height: 65%;
            width: 60%;
            border-radius: 10px;
            min-width: 400px;
            margin: 20px;
          "
        >
          <template #header>
            <el-row justify="space-between">
              <span style="font-weight: bold">My Upcoming Inspection</span>
              <span
                style="font-weight: bold"
               
                >{{ inspection_date }}</span
              ><el-button
                v-if="
                  this.$root.user_role() === 'tenant' &&
                  inspection_date !== null
                "
                size="mini"
                type="danger"
                round
                plain
                @click="rejectInspectionTenant"
                >Reject</el-button
              ><el-button
                v-if="
                  this.$root.user_role() === 'manager' &&
                  inspection_date !== null
                "
                size="mini"
                type="primary"
                round
                plain
                @click="showPlan"
                >Show</el-button
              ><span v-if="inspection_date === null"
                >You do not have any future inspection.</span
              >
            </el-row>
          </template>
          <el-calendar>
            <template v-if="inspection_date" #dateCell="{ data }">
              {{ data.day.split("-")[2] }}
              <div
                v-if="data.day === inspection_date.split(' ')[0]"
                style="
                  font-weight: bold;
                  color: white;
                  background-color: #788f77;
                  border-radius: 3px;
                  text-align: center;
                "
              >
                {{ inspection_date.split(" ")[1] }}
              </div>
            </template>
          </el-calendar></el-card
        >
        <el-card
          class="profile-container"
          style="height: 560px; width: 420px; border-radius: 10px; margin: 20px"
        >
          <profile @inspection-day="getInspection" />
        </el-card>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import AddressInput from "../components/GoogleMaps/addressInput.vue";
import Profile from "../components/Profile.vue";
import { APIurl } from "@/http";
import { ElMessage } from "element-plus";
export default {
  components: { Profile, AddressInput },
  name: "Index",
  data() {
    return {
      inspection_date: null,
    };
  },
  methods: {
    getInspection(date) {
      this.inspection_date = date;
      return true;
    },
    showPlan() {
      this.$router.push("/plan");
    },
    rejectInspectionTenant() {
      this.$axios
        .post(APIurl + "/plan/tenant_reject", {
          id: localStorage.getItem("id"),
        })
        .then((response) => {
          if (response.status === 200) {
            ElMessage({
              message: "Reject inspection successfully.",
              type: "success",
              center: true,
            });
            location.reload();
          }
        });
    },
  },
};
</script>


<style scoped>
.not-login-container {
  background-image: url("../assets/loginbg1.jpg");
  background-size: cover;
  background-position: center;
  height: 100vh;
}

.not-login {
  width: 100%;
  height: 100%;
}

.el-calendar :deep(.el-calendar-table .el-calendar-day) {
  height: 9.5vh;
  width: 7vw;
}

.index-container :deep(.el-card__body) {
  padding: 0px;
}

.profile-container :deep(.el-card__body) {
  padding: 10px;
}
</style>
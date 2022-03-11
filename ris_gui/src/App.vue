<template>
  <div class="main-bg" v-if="logged">
    <el-header style="margin-top: 10px" v-if="user_role() === 'manager'">
      <el-row align="middle" style="border: solid #365638; border-radius: 10px">
        <el-col :xs="18" :sm="22" :md="22" :lg="22" :xl="23">
          <el-menu
            style="border-radius: 10px"
            mode="horizontal"
            text-color="darkgreen"
            active-text-color="#365638"
            router
            :default-active="this.$route.path"
          >
            <el-menu-item index="/">
              <img src="../public/logo1.png" height="35" width="35" />
            </el-menu-item>
            <el-menu-item index="/myproperties">
              <!-- <i class="el-icon-office-building" /> -->
              <font-awesome-icon icon="building" /> &nbsp; &nbsp;
              <span>My Properties</span>
            </el-menu-item>
            <el-menu-item index="/newproperties">
              <!-- <i class="el-icon-info" /> -->
              <font-awesome-icon icon="plus-square" /> &nbsp; &nbsp;
              <span>Add Properties</span>
            </el-menu-item>
            <el-menu-item index="/plan">
            <!-- <i class="el-icon-date" /> -->
              <font-awesome-icon icon="route" /> &nbsp; &nbsp;
              <span> Itinerary Plan</span>
            </el-menu-item>
            <el-menu-item index="/reportOverview">
              <i class="el-icon-collection" />
              <span>Inspection Report Overview</span>
            </el-menu-item>
          </el-menu>
        </el-col>
        <el-col :xs="5" :sm="2" :md="2" :lg="2" :xl="1"
          ><el-row justify="end" style="margin-right: 10px"
            ><user-bar
          /></el-row>
        </el-col>
      </el-row>
    </el-header>
    <el-header
      v-else
      style="
        margin-top: 10px;
        border: solid #365638;
        border-radius: 10px;
        margin: 10px 20px 3px 20px;
        height: 7vh;
        min-height: 60px;
      "
      ><el-row justify="space-between" align="middle" style="height: 50px"
        ><img src="../public/logo1.png" height="45" width="45" /><span
          style="color: #365638; font-size: 2vw; font-weight: bold"
          >WELCOME TO RENTAL INSPECTION SYSTEM</span
        >
        <el-button round plain type="danger"><logout /></el-button
      ></el-row>
    </el-header>
    <el-main> <router-view /><el-backtop /> </el-main>
  </div>
  <div v-else class="login-page">
    <router-view />
  </div>
</template>

<script>
import { ref, reactive } from "vue";
import UserBar from "./components/UserBar.vue";
import Logout from "./components/auth/Logout.vue";
import {
  faBuilding,
  faPlusSquare,
  faRoute,
} from "@fortawesome/free-solid-svg-icons";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
library.add(faBuilding, faPlusSquare, faRoute);
export default {
  components: { UserBar, Logout, FontAwesomeIcon },
  data() {
    return {
      logged: ref(this.loggedOn()),
      role: ref(this.user_role()),
    };
  },
  methods: {
    loggedOn() {
      return localStorage.getItem("Token") ? true : false;
    },
    user_role() {
      return this.loggedOn() ? localStorage.getItem("role") : "";
    },
  },
};
</script>

<style scoped>
/* #365638 */
/* #788F77 */
/* html {
  font-family: Arial, Helvetica, sans-serif;
  margin: 0%;
} */
</style>
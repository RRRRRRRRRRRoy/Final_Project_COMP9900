<template>
  <div>
    <el-dropdown>
      <el-avatar :src="avatar"></el-avatar>
      <template #dropdown>
        <el-dropdown-menu>
          <el-dropdown-item
            ><div @click="showProfile">Homepage</div></el-dropdown-item
          >
          <!-- <el-dropdown-item
            ><div @click="showProfile">Profile</div></el-dropdown-item
          > -->
          <el-dropdown-item> <logout /></el-dropdown-item>
        </el-dropdown-menu>
      </template>
    </el-dropdown>
    <!-- <el-drawer
      v-model="profile"
      title="My profile"
      direction="rtl"
      show-close
      size="50"
    >
      <profile />
    </el-drawer> -->
  </div>
</template>

<script>
import Logout from "./auth/Logout.vue";
// import Profile from "./Profile.vue";

export default {
  components: { Logout },
  name: "UserBar",
  data() {
    return {
      avatar: localStorage.getItem("avatar"),
    };
  },
  methods: {
    showProfile() {
      this.$router.push("/");
    },
  },
};
</script>

<style>
</style>
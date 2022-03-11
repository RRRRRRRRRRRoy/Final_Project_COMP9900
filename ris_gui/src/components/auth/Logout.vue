<template>
  <div @click="signOut">Logout</div>
</template>

<script>
import { ElMessage } from "element-plus";
import { APIurl } from "@/http";

export default {
  methods: {
    signOut() {
      this.$axios.get(APIurl + "/auth/logout").then((response) => {
        if (response.status == 200) {
          // localStorage.removeItem("Token");
          // localStorage.removeItem("User");
          // localStorage.removeItem("avatar");
          localStorage.clear();
          sessionStorage.clear();
          // this.$root.currentUser = {
          //   id: "",
          //   name: "",
          //   role: "",
          //   avatar: "",
          //   email: "",
          //   mobile: "",
          // };
          this.$root.logged = false;
          window.location.reload();
          this.$router.push("/login");
          ElMessage({
            showClose: true,
            message: "Logout successfully.",
            type: "success",
            center: true,
          });
        }
      });
    },
  },
};
</script>

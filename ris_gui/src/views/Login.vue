<template>
  <div class="login-page">
    <el-row style="height: 100vh" justify="center" align="middle">
      <el-card shadow="hover" class="login-card"
        ><el-header>
          <el-row justify="center"
            ><el-link href="/" :underline="false">
              <img
                src="../assets/logo1.png"
                height="70"
                width="70" /></el-link></el-row></el-header
        ><el-row style="height: 20px"></el-row
        ><el-main>
          <el-form
            ref="loginForm"
            :model="loginForm"
            label-width="0"
            label-position="left"
            :rules="rules"
            size="medium"
          >
            <!-- Choose the role -->
            <el-form-item prop="role">
              <el-row justify="center" :gutter="30">
                <el-radio-group v-model="loginForm.role" fill="#365638">
                  <el-col>
                    <el-radio-button label="manager"
                      ><el-row
                        class="role-card"
                        justify="center"
                        align="middle"
                      >
                        <div style="font-size: 10px">I'M A</div>
                        <div style="font-weight: bold">MANAGER</div>
                      </el-row>
                    </el-radio-button> </el-col
                  ><el-col>
                    <el-radio-button label="tenant"
                      ><el-row
                        class="role-card"
                        justify="center"
                        align="middle"
                      >
                        <div style="font-size: 10px">I'M A</div>
                        <div style="font-weight: bold">TENANT</div>
                      </el-row>
                    </el-radio-button>
                  </el-col>
                </el-radio-group>
              </el-row>
            </el-form-item>
            <!-- Enter email address -->
            <el-form-item prop="email"
              ><el-row justify="center">
                <el-autocomplete
                  v-model="loginForm.email"
                  style="width: 246px"
                  placeholder="Email"
                  :fetch-suggestions="querySearch"
                  clearable
                  :trigger-on-focus="false"
                >
                  <template #prefix
                    ><i class="el-icon-message" style="color: #365638"></i
                  ></template>
                </el-autocomplete>
              </el-row>
            </el-form-item>
            <!-- Enter password -->
            <el-form-item prop="password" :show-message="false"
              ><el-row justify="center">
                <el-input
                  class="login-input"
                  v-model="loginForm.password"
                  placeholder="Password"
                  show-password
                  clearable
                  ><template #prefix
                    ><i
                      class="el-icon-key"
                      style="color: #365638"
                    ></i></template></el-input
              ></el-row>
              <el-row justify="end" align="top" style="height: 5px"
                ><el-link
                  href="/forgot"
                  :underline="false"
                  style="font-size: 3px; font-weight: bold; color: #365638"
                >
                  FORGOT PASSWORD?
                </el-link></el-row
              >
            </el-form-item>

            <!-- Login button -->
            <el-form-item
              ><el-row justify="center">
                <el-button
                  class="login-button"
                  @click="signIn('loginForm')"
                  v-loading="logInLoading"
                  element-loading-spinner="el-icon-loading"
                  element-loading-background="rgba(0, 0, 0, 0.8)"
                  >SIGN IN
                  <span v-if="loginForm.role !== ''"
                    >AS A {{ loginForm.role.toUpperCase() }}</span
                  >
                </el-button></el-row
              >
            </el-form-item>
            <el-row style="width: 246px" justify="center">
              <span style="font-size: 10px; color: #365638"
                >NEW TO HERE? &nbsp;</span
              >
              <el-link
                href="/register"
                :underline="false"
                style="font-size: 10px; font-weight: bold; color: #365638"
              >
                REGISTER
              </el-link>
            </el-row>
          </el-form></el-main
        ></el-card
      >
    </el-row>
  </div>
</template>

<script>
import { ElMessage } from "element-plus";
import { APIurl } from "@/http";
import { ref } from "vue";
import { emailPostfix } from "../utils/formValidator/emailFormatCheck";
export default {
  data() {
    return {
      emailSuffix: emailPostfix,
      loginForm: {
        email: "",
        password: "",
        role: "",
      },
      rules: {
        role: [
          {
            required: true,
            message: "Please select your role.",
            trigger: "blur",
          },
        ],
        email: [
          {
            required: true,
            message: "Please enter the email.",
            trigger: "change",
          },
          {
            // validator: emailFormatCheck,
            type: "email",
            message: "Invalid email format.",
            trigger: "blur",
          },
        ],
        password: [
          {
            required: true,
            message: "Please enter the password.",
            trigger: "blur",
          },
        ],
      },
      logInLoading: ref(false),
    };
  },
  methods: {
    querySearch(queryString, callback) {
      if (queryString === "") {
        callback([]);
      } else if (!/@/.test(queryString)) {
        const results = new Array();
        this.emailSuffix.forEach((element) => {
          results.push({ value: queryString + element });
        });
        callback(results);
      } else {
        callback([]);
      }
    },
    toRegister() {
      this.$router.push("/register");
    },
    toForgot() {
      this.$router.push("/forgot");
    },
    signIn(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.logInLoading = true;
          this.$axios
            .post(APIurl + "/auth/login", this.loginForm)
            .then((response) => {
              if (response.status === 200) {
                this.logInLoading = false;
                localStorage.setItem("id", response.data.id);
                localStorage.setItem("role", this.loginForm.role);
                localStorage.setItem("avatar", response.data.avatar);
                localStorage.setItem("Token", response.data.token);
                ElMessage({
                  showClose: true,
                  message: "Login successfully.",
                  type: "success",
                  center: true,
                });
                this.$root.logged = true;
                this.$router.push("/");
              }
            })
            .catch((error) => {
              if (
                error.response.status === 400 ||
                error.response.status === 404
              ) {
                this.logInLoading = false;
                this.loginForm.password = "";
                ElMessage({
                  showClose: true,
                  message: "Invalid email or password.",
                  type: "error",
                  center: true,
                });
              }
            });
        }
      });
    },
  },
};
</script>

<style scoped>
.role-card {
  width: 65px;
  height: 25px;
  border: 0;
  margin: 0;
  padding: 0;
}
.login-card {
  width: 325px;
  height: 400px;
  filter: saturate(80%);
  border-style: none;
  background-color: rgba(83, 244, 255, 0.3);
}
.login-input {
  color: #365638;
  width: 246px;
  text-decoration-color: #365638;
  font-weight: bold;
}
.login-button {
  width: 246px;
  background-color: #365638;
  color: #ffffff;
  border: none;
}
.el-card:hover {
  background-color: rgba(255, 255, 255, 0.95);
}
.login-tips {
  text-size-adjust: 10px;
}
.login-page {
  background-image: url("../assets/loginbg1.jpg");
  background-size: cover;
  background-position: center;
}
.el-autocomplete {
  background-color: #365638;
}
</style>
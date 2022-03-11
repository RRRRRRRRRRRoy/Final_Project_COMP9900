<template>
  <div class="login-page">
    <el-row style="height: 100vh" justify="center" align="middle">
      <el-card shadow="hover" class="login-card"
        ><el-header>
          <el-row justify="center"
            ><el-link href="/" :underline="false">
              <img
                src="../assets/logo1.png"
                height="100"
                width="100" /></el-link></el-row></el-header
        ><el-row style="height: 60px"></el-row
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
              <el-row justify="center">
                <select-role
                  :role="loginForm.role"
                  :roleBoxStyle="roleBoxStyle"
                  @changeRole="getRole"
                />
              </el-row>
            </el-form-item>
            <!-- Enter email address -->
            <el-form-item prop="email"
              ><el-row justify="center">
                <el-popover
                  placement="bottom"
                  :show-arrow="false"
                  :width="220"
                  :offset="0"
                  :visible="
                    loginForm.email !== '' && !/@/.test(loginForm.email)
                  "
                  trigger="focus"
                >
                  <template #reference>
                    <el-input
                      v-model="loginForm.email"
                      clearable
                      placeholder="EMAIL"
                      class="login-input"
                    >
                      <template #prefix
                        ><i
                          class="el-input__icon el-icon-message"
                          style="color: #365638; font-weight: bold"
                        ></i
                      ></template>
                    </el-input>
                  </template>
                  <div v-for="suffix in emailC" :key="suffix">
                    <div
                      style="font-weight: bold; color: #365638; cursor: pointer"
                      @click="completeEmail(suffix.value)"
                    >
                      {{ loginForm.email }}{{ suffix.value }}
                    </div>
                  </div>
                </el-popover>
              </el-row>
            </el-form-item>
            <!-- Enter password -->
            <el-form-item prop="password" style="margin-bottom: 0"
              ><el-row justify="center">
                <el-input
                  class="login-input"
                  v-model="loginForm.password"
                  show-password
                  clearable
                  placeholder="PASSWORD"
                  @keydown.enter="signIn('loginForm')"
                >
                  <template #prefix
                    ><i
                      class="el-input__icon el-icon-key"
                      style="color: #365638; font-weight: bold"
                    ></i></template
                ></el-input>
              </el-row>
            </el-form-item>
            <el-row
              justify="end"
              style="
                height: 20px;
                width: 280px;
                margin-top: 0;
                margin-bottom: 2px;
              "
              ><el-link
                href="/forgot"
                :underline="false"
                style="font-size: 12px; color: #788f77"
              >
                FORGOT PASSWORD?
              </el-link></el-row
            >
            <!-- Login button -->
            <el-form-item
              ><el-row justify="center">
                <el-button
                  class="login-button"
                  @click="signIn('loginForm')"
                  v-loading="logInLoading"
                  >SIGN IN
                  <span v-if="loginForm.role !== ''"
                    >AS A {{ loginForm.role.toUpperCase() }}</span
                  >
                </el-button></el-row
              >
            </el-form-item>
            <el-row style="width: 280px" justify="center">
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
import { reactive, ref } from "vue";
import { emailSuffix } from "../utils/formValidator/emailFormatCheck";
import SelectRole from "../components/auth/selectRole.vue";

export default {
  components: { SelectRole },

  data() {
    return {
      emailC: emailSuffix,
      currentRow: null,
      loginForm: reactive({
        email: "",
        password: "",
        role: "",
      }),
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
            message: "Please enter your email.",
            trigger: "change",
          },
          {
            // validator: emailFormatCheck,
            type: "email",
            message: "Invalid email format.",
            trigger: "change",
          },
        ],
        password: [
          {
            required: true,
            message: "Please enter password.",
            trigger: "blur",
          },
        ],
      },
      logInLoading: ref(false),
      logInClicked: ref(false),
    };
  },
  methods: {
    getRole(role) {
      this.loginForm.role = role;
      return true;
    },
    signIn(formName) {
      this.logInClicked = true;
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
                if (response.data.avatar === "") {
                  localStorage.setItem(
                    "avatar",
                    "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
                  );
                } else {
                  localStorage.setItem("avatar", response.data.avatar);
                }
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
    completeEmail(row) {
      this.loginForm.email += row;
    },
  },
  computed: {
    managerStyle() {
      return this.loginForm.role === "manager" ? "#ffffff" : "#788f77";
    },
    tenantStyle() {
      return this.loginForm.role === "tenant" ? "#ffffff" : "#788f77";
    },
    roleBoxStyle() {
      return this.logInClicked && this.loginForm.role === ""
        ? "#f56c6c"
        : "#365638";
    },
  },
};
</script>

<style scoped>
.login-card {
  width: 360px;
  height: 510px;
  filter: saturate(80%);
  border-style: none;
  background-color: rgba(83, 244, 255, 0.3);
}

.login-input :deep(input) {
  color: #365638;
  font-weight: bold;
  border: solid #365638;
  height: 40px;
}

.login-input :deep(input::-webkit-input-placeholder) {
  color: #788f77;
}

.login-button {
  width: 100%;
  height: 70px;
  background-color: #365638;
  color: #ffffff;
  border: none;
  font-weight: bold;
  font-size: 16px;
  margin-top: 15px;
}

.el-card:hover {
  background-color: rgba(255, 255, 255, 0.95);
  border: solid #365638 3px;
  border-radius: 10px;
}

.login-page {
  background-image: url("../assets/loginbg1.jpg");
  background-size: cover;
  background-position: center;
}
</style>
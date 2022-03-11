<template>
  <div>
    <el-row justify="space-around">
      <el-dialog
        v-model="dialogVisible"
        title="No Properties"
        width="30%"
        :show-close="false"
        :close-on-click-modal="false"
      >
        <span>You did not add any properties, please add for further use.</span>
        <template #footer
          ><el-row justify="space-between" style="width: 200px">
            <span>
              <el-link
                href="/"
                type="success"
                :underline="false"
                icon="el-icon-house"
                >Homepage
              </el-link>
            </span>
            <span>
              <el-link
                href="/NewProperties"
                type="primary"
                :underline="false"
                icon="el-icon-plus"
                >Add Properties
              </el-link>
            </span>
          </el-row>
        </template>
      </el-dialog>
      <el-col :span="15" v-if="!dialogVisible">
        <div id="map" style="width: 100%; height: 86vh; border-radius: 10px" />
        <div id="scale-tools" class="scale-tools">
          <el-row justify="space-between"
            ><el-tooltip content="Reset" placement="bottom" effect="light">
              <i
                class="el-icon-refresh"
                style="cursor: pointer; font-weight: bold"
                @click="reset" /></el-tooltip
            ><el-tooltip
              content="Location Scale"
              placement="bottom"
              effect="light"
            >
              <i
                class="el-icon-office-building"
                style="cursor: pointer; font-weight: bold"
                @click="rescale" /></el-tooltip
            ><el-tooltip content="Route Scale" placement="bottom" effect="light"
              ><i
                class="el-icon-guide"
                style="cursor: pointer; font-weight: bold"
                @click="routeScale" /></el-tooltip
          ></el-row>
        </div>
        <div id="legend" class="legend">
          <el-descriptions title="Legend" :column="1" size="small">
            <el-descriptions-item label-align="center">
              <template #label
                ><font-awesome-icon
                  icon="thumbtack"
                  style="
                    color: red;
                    font-size: 15px;
                    width: 12px;
                    text-align: center;
                  "
              /></template>
              <span>Selected Properties</span>
            </el-descriptions-item>
            <el-descriptions-item label-align="center">
              <template #label
                ><font-awesome-icon
                  icon="thumbtack"
                  style="color: deeppink; width: 12px; text-align: center"
              /></template>
              <span>Unselected Properties</span>
            </el-descriptions-item>
            <el-descriptions-item label-align="center">
              <template #label
                ><font-awesome-icon
                  icon="map-pin"
                  style="color: orangered; width: 12px; text-align: center"
              /></template>
              <span>Preferred Start Location</span>
            </el-descriptions-item>
            <el-descriptions-item label-align="center">
              <template #label
                ><font-awesome-icon
                  icon="map-marker"
                  style="color: red; width: 12px; text-align: center"
              /></template>
              <span>Start Location</span>
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </el-col>
      <el-col :span="8" v-if="!dialogVisible"
        ><el-space direction="vertical">
          <el-card style="min-width: 430px; border-radius: 10px">
            <template #header
              ><font-awesome-icon icon="route" /> &nbsp; Itinerary Planning
            </template>
            <el-alert
              v-if="completeAlert"
              title="Please make sure time and addresses are not empty."
              type="warning"
            />
            <el-row>
              <!-- <el-button @click="planRoute" type="primary" round plain
                >Generate Directions</el-button
              > -->
              <el-button
                @click="submitPlan"
                type="success"
                round
                plain
                size="mini"
                :disabled="completeAlert"
                >Show & Submit</el-button
              >
              <el-button
                @click="Cancel"
                type="danger"
                round
                plain
                size="mini"
                v-if="plan"
                >Cancel</el-button
              >
              <el-button @click="reset" type="warning" round plain size="mini"
                >Reset</el-button
              >
            </el-row>
          </el-card>
          <el-card style="min-width: 430px; border-radius: 10px">
            <template #header>
              <el-row justify="space-between" align="middle"
                ><div>Departure Options</div>
                <el-select
                  v-model="startMode"
                  placeholder="Select departure address"
                  @change="changeStartMode"
                >
                  <el-option label="use current location" :value="0" />
                  <el-option label="use my preferred addresses" :value="1" />
                  <el-option
                    label="manually input address"
                    :value="2"
                  /> </el-select></el-row
            ></template>
            <el-row justify="space-between" align="middle"
              ><span>Time</span
              ><span v-if="timeAlert" style="color: #f56c6c; font-weight: bold"
                ><i class="el-icon-warning" /> Please select a time in the
                future.</span
              ></el-row
            >
            <el-date-picker
              style="width: 100%"
              v-model="inPlan.time"
              type="datetime"
              placeholder="Select departure date and time"
              :shortcuts="DTPicker"
              :editable="false"
              @change="changeTime"
            />
            <el-row justify="space-between"
              ><span>Address</span
              ><span v-if="startMode === 2 && lastAddrBuffer.manual">{{
                lastAddrBuffer.manual.formatted_address.replace(
                  ", Australia",
                  ""
                )
              }}</span>
            </el-row>
            <address-input
              id="a"
              v-if="startMode === 2"
              @get-address="getManual"
              @clear-address="clearManual"
            />
            <el-input
              v-if="startMode === 0"
              v-model="lastAddrBuffer.current.formatted_address"
              readonly
              style="width: 100%"
              v-loading="freshCurrentLoading"
            >
              <template #append>
                <span @click="refreshCurrent" style="cursor: pointer"
                  ><i class="el-icon-refresh"
                /></span>
              </template>
            </el-input>
            <el-select
              v-if="startMode === 1"
              v-model="inPlan.start"
              style="width: 100%"
              filterable
              placeholder="Select your preferred address"
              @change="changeStart"
              clearable
            >
              <el-option
                v-for="(value, key) in addr.start"
                :key="key"
                :value="value"
                :label="'Marked on the map.'"
              >
                <span style="float: left">{{
                  value.formatted_address.split(", ")[0]
                }}</span>
                <span
                  style="
                    float: right;
                    color: var(--el-text-color-secondary);
                    font-size: 13px;
                  "
                  >{{ value.formatted_address.split(", ")[1] }}</span
                >
              </el-option>
            </el-select>
          </el-card>
          <el-card style="min-width: 430px; border-radius: 10px">
            <template #header> Properties Options</template>
            <el-row>Enter duration for each property (max 60 mins)</el-row>
            <el-row justify="space-between" align="middle">
              <el-input-number
                v-model="inPlan.duration"
                clearable
                placeholder="Inpection Duration"
                style="width: 70%"
                :min="10"
                :max="60"
                :step="5"
                controls-position="right"
              >
                <template #append>min</template> </el-input-number
              ><span style="width: 25%">minutes</span></el-row
            >
            <el-row>Select properties</el-row>
            <el-select
              v-model="inPlan.places"
              multiple
              style="width: 100%"
              filterable
              clearable
              placeholder="Select properties"
              :multiple-limit="6"
              @change="changePlace"
            >
              <el-option
                v-for="(value, key) in addr.properties"
                :key="key"
                :label="value.formatted_address.replace(', Australia', '')"
                :value="key"
              >
                <span style="float: left">{{
                  value.formatted_address.split(", ")[
                    (0, value.formatted_address.split(", ").length - 3)
                  ]
                }}</span>
                <span
                  style="
                    float: right;
                    color: var(--el-text-color-secondary);
                    font-size: 13px;
                  "
                >
                  {{
                    value.formatted_address.split(", ")[
                      value.formatted_address.split(", ").length - 2
                    ]
                  }}
                </span>
              </el-option>
            </el-select>
          </el-card>
        </el-space>
      </el-col>
    </el-row>
  </div>
</template>


<script>
import {
  defineComponent,
  onMounted,
  ref,
  reactive,
  watch,
  watchEffect,
} from "vue";
import {
  faThumbtack,
  faMapPin,
  faMapMarker,
  faRoute,
} from "@fortawesome/free-solid-svg-icons";
import { library } from "@fortawesome/fontawesome-svg-core";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { ElMessage, ElMessageBox } from "element-plus";
import axios from "axios";
import moment from "moment";
import { APIurl } from "@/http";
import addressInput from "./GoogleMaps/addressInput.vue";
library.add(faThumbtack, faMapPin, faMapMarker, faRoute);
export default defineComponent({
  components: { addressInput, FontAwesomeIcon },
  setup() {
    const dialogVisible = ref(false);
    var addr = {
      start: {},
      properties: {},
    };
    const inPlan = reactive({
      start: null,
      places: [],
      time: null,
      duration: 20,
    });
    const map = ref(null);
    const bounds = ref(null);
    const setBounds = (additional) => {
      bounds.value = new google.maps.LatLngBounds();
      for (let s in addr.start) {
        bounds.value.extend(addr.start[s].loc);
      }
      for (let p in addr.properties) {
        bounds.value.extend(addr.properties[p].loc);
      }
      if (additional) {
        bounds.value.extend(additional);
      }
      map.value.fitBounds(bounds.value);
      map.value.setCenter(bounds.value.getCenter());
    };
    const freshCurrentLoading = ref(false);
    var marker_start = [];
    var marker_properties = {};
    var marker_manual = null;

    onMounted(() => {
      let propAddr = localStorage.getItem("property_addr");
      if (propAddr == "null" || propAddr === "{}") {
        dialogVisible.value = true;
      } else {
        let s = {};
        let sa = JSON.parse(localStorage.getItem("start_address"));
        let si = 1;
        for (let i in sa) {
          if (sa[i]) {
            s[si] = sa[i];
            si += 1;
          }
        }
        addr.start = s;
        addr.properties = JSON.parse(localStorage.getItem("property_addr"));
        let scale_tools = document.getElementById("scale-tools");
        let legend = document.getElementById("legend");
        map.value = new google.maps.Map(document.getElementById("map"), {
          zoom: 10,
          center: { lat: -33.85, lng: 151.11 },
          fullScreenControl: false,
          streetViewControl: false,
          styles: [
            {
              featureType: "poi.business",
              stylers: [{ visibility: "off" }],
            },
            {
              featureType: "transit",
              elementType: "labels.icon",
              stylers: [{ visibility: "off" }],
            },
          ],
        });
        map.value.controls[google.maps.ControlPosition.RIGHT].push(scale_tools);
        map.value.controls[google.maps.ControlPosition.LEFT].push(legend);
        init();
        if (localStorage.getItem("plan") !== "null") {
          let p = JSON.parse(localStorage.getItem("plan")).inPlan;
          inPlan.start = p.start;
          inPlan.places = p.places;
          inPlan.duration = p.duration;
          inPlan.time = null;
        }
      }
    });
    const init = () => {
      marker_start = [];
      marker_properties = [];
      if (marker_manual) {
        marker_manual.setMap(null);
        marker_manual = null;
      }
      for (let s in addr.start) {
        marker_start.push(
          new google.maps.Marker({
            animation: google.maps.Animation.DROP,
            label: s,
            optimized: true,
            position: addr.start[s].loc,
            map: map.value,
            title:
              `Start ${s}: ` +
              addr.start[s].formatted_address.replace(", Australia", ""),
            icon: {
              path: faMapPin.icon[4],
              fillColor: "orangered",
              fillOpacity: 1,
              strokeWeight: 1,
              strokeColor: "#ffffff",
              scale: 0.05,
              anchor: new google.maps.Point(
                faMapPin.icon[0] / 2, // width
                faMapPin.icon[1] // height
              ),
            },
          })
        );
      }
      for (let p in addr.properties) {
        marker_properties[p] = new google.maps.Marker({
          id: p,
          animation: google.maps.Animation.DROP,
          optimized: true,
          position: addr.properties[p].loc,
          map: map.value,
          title:
            "Property: " +
            addr.properties[p].formatted_address.replace(", Australia", ""),
          icon: {
            path: faThumbtack.icon[4],
            fillColor: "deeppink",
            fillOpacity: 1,
            strokeWeight: 1,
            strokeColor: "#ffffff",
            scale: 0.05,
            anchor: new google.maps.Point(
              faThumbtack.icon[0] / 2, // width
              faThumbtack.icon[1] // height
            ),
          },
        });
      }
      setBounds(null);
    };

    const refreshCurrent = () => {
      freshCurrentLoading.value = true;
      if (navigator.geolocation) {
        let geocoder = new google.maps.Geocoder();
        navigator.geolocation.getCurrentPosition((position) => {
          let loc = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          geocoder.geocode({ location: loc }).then((response) => {
            lastAddrBuffer.current.formatted_address =
              "near " + response.results[0].formatted_address;
            lastAddrBuffer.current.loc = loc;
            inPlan.start = lastAddrBuffer.current;
            setStartMarker({
              loc: loc,
              formatted_address:
                "near " + response.results[0].formatted_address,
            });
          });
        });
      } else {
        alert("Your browser does not support Geolocation");
      }
      freshCurrentLoading.value = false;
    };
    const startMode = ref(1);
    const lastAddrBuffer = reactive({
      current: { loc: null, formatted_address: null },
      prefer: null,
      manual: null,
    });
    const setStartMarker = (addr) => {
      if (marker_manual) {
        marker_manual.setMap(null);
        marker_manual = null;
      }
      if (addr) {
        marker_manual = new google.maps.Marker({
          animation: google.maps.Animation.DROP,
          optimized: true,
          position: addr.loc,
          map: map.value,
          title: `Start@ ` + addr.formatted_address,
          icon: {
            path: faMapMarker.icon[4],
            fillColor: "orangered",
            fillOpacity: 1,
            strokeWeight: 1,
            strokeColor: "#ffffff",
            scale: 0.05,
            anchor: new google.maps.Point(
              faMapMarker.icon[0] / 2, // width
              faMapMarker.icon[1] // height
            ),
          },
        });
        setBounds(addr.loc);
      } else {
        setBounds(null);
      }
    };
    const changeStartMode = (val) => {
      if (val === 0) {
        if (lastAddrBuffer.current.loc) {
          inPlan.start = lastAddrBuffer.current;
          setStartMarker(lastAddrBuffer.current);
        } else {
          refreshCurrent();
        }
      } else if (val === 1) {
        if (lastAddrBuffer.prefer) {
          inPlan.start = lastAddrBuffer.prefer;
          setStartMarker(addr.start[lastAddrBuffer.prefer]);
        } else {
          inPlan.start = null;
          setStartMarker(null);
          if (marker_manual) {
            marker_manual.setMap(null);
            marker_manual = null;
          }
        }
      } else if (val === 2) {
        if (lastAddrBuffer.manual) {
          inPlan.start = lastAddrBuffer.manual;
          setStartMarker(lastAddrBuffer.manual);
        } else {
          inPlan.start = null;
          setStartMarker(null);
          if (marker_manual) {
            marker_manual.setMap(null);
            marker_manual = null;
          }
        }
      }
    };

    const getManual = (data, id) => {
      if (marker_manual) {
        marker_manual.setMap(null);
        marker_manual = null;
        setBounds(null);
      }
      lastAddrBuffer.manual = data;
      inPlan.start = data;
      marker_manual = new google.maps.Marker({
        animation: google.maps.Animation.DROP,
        optimized: true,
        position: data.loc,
        map: map.value,
        title: data.formatted_address.replace(", Australia", ""),
      });
      setBounds(data.loc);
    };
    const clearManual = () => {
      if (marker_manual) {
        marker_manual.setMap(null);
        marker_manual = null;
      }
    };
    const getGeo = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
          let pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };
          return pos;
        });
      } else {
        alert("Your browser does not support Geolocation");
      }
    };

    const changeTime = (val) => {
      let now = new Date();
      let d = new Date(val);
      if (val === null) {
        timeAlert.value = false;
        return;
      }
      if (now.getTime() >= d.getTime()) {
        inPlan.time = null;
        timeAlert.value = true;
      } else {
        timeAlert.value = false;
      }
    };
    const changePlace = (val) => {
      for (let p in marker_properties) {
        marker_properties[p].setMap(null);
        marker_properties[p].icon.fillColor = "deeppink";
        marker_properties[p].icon.scale = 0.04;
        marker_properties[p].setMap(map.value);
      }
      val.forEach((value) => {
        marker_properties[value].setMap(null);
        marker_properties[value].icon.fillColor = "red";
        marker_properties[value].icon.scale = 0.06;
        marker_properties[value].setMap(map.value);
      });
    };
    const changeStart = (value) => {
      setStartMarker(value);
      lastAddrBuffer.prefer = value;
      inPlan.start = value;
    };
    const DTPicker = [
      {
        text: "15 min later",
        value: () => {
          const date = new Date();
          date.setTime(date.getTime() + 15 * 60 * 1000);
          return date;
        },
      },
      {
        text: "30 min later",
        value: () => {
          const date = new Date();
          date.setTime(date.getTime() + 30 * 60 * 1000);
          return date;
        },
      },
      {
        text: "1 hour later",
        value: () => {
          const date = new Date();
          date.setTime(date.getTime() + 60 * 60 * 1000);
          return date;
        },
      },
      {
        text: "2 hours later",
        value: () => {
          const date = new Date();
          date.setTime(date.getTime() + 2 * 60 * 60 * 1000);
          return date;
        },
      },
    ];
    const timeAlert = ref(null);
    const completeAlert = ref(false);
    const plan = ref(null);
    const plan_result = ref(null);
    const directionsRenderer = ref(null);
    const generateRoute = (terminate, wayP, time) => {
      plan.value = new google.maps.DirectionsService();
      directionsRenderer.value = new google.maps.DirectionsRenderer();
      plan.value
        .route({
          origin: terminate,
          destination: terminate,
          waypoints: wayP,
          optimizeWaypoints: true,
          provideRouteAlternatives: true,
          travelMode: google.maps.TravelMode.DRIVING,
          drivingOptions: {
            departureTime: time,
          },
        })
        .then((result) => {
          if (result.status === google.maps.DirectionsStatus.OK) {
            plan_result.value = result;
            directionsRenderer.value.setDirections(result);
            directionsRenderer.value.setMap(map.value);
          }
        })
        .catch((error) => {
          if (error.code === google.maps.DirectionsStatus.ZERO_RESULTS) {
            ElMessage({
              showClose: true,
              type: "error",
              message: "Sorry, there seems no routes.",
              center: true,
              duration: 6000,
            });
          }
        });
    };
    const planRoute = () => {
      if (
        inPlan.start === null ||
        inPlan.places.length === 0 ||
        inPlan.time === null
      ) {
        completeAlert.value = true;
        return;
      }
      completeAlert.value = false;
      let terminate = inPlan.start.formatted_address;
      let viaPlace = new Array();
      let dTime = null;
      inPlan.places.forEach((val) => {
        viaPlace.push({ location: addr.properties[val].formatted_address, stopover: true });
      });
      dTime = inPlan.time;
      generateRoute(terminate, viaPlace, dTime);
    };
    const submitPlan = () => {
      ElMessageBox.confirm("Your plan will be covered!", "Warning", {
        confirmButtonText: "Confirm",
        cancelButtonText: "Cancel",
        type: "warning",
      }).then(() => {
        if (plan_result.value) {
          let propertyList = [];
          let destinations = [
            inPlan.start.formatted_address,
            inPlan.start.formatted_address,
          ];
          for (let i in inPlan.places) {
            propertyList.push(addr.properties[inPlan.places[i]].pid);
          }
          let t = new moment(inPlan.time);
          let form = {
            id: Number(localStorage.getItem("id")),
            day: t.format("yyyy-MM-DD kk:mm:ss").replace(/ 24\:/, " 00:"),
            plan: JSON.stringify(plan_result.value),
            p_list: propertyList.join("|||"),
            duration: String(inPlan.duration),
            destinations: destinations.join("|||"),
            inPlan: JSON.stringify(inPlan),
          };

          axios
            .post(APIurl + "/plan/store", form)
            .then((response) => {
              if (response.status === 200) {
                ElMessage({
                  type: "success",
                  message: "Successfully submit plan.",
                  center: true,
                });
                let t = new moment(inPlan.time);
                localStorage.setItem(
                  "plan",
                  JSON.stringify({
                    plan: plan_result.value,
                    duration: inPlan.duration,
                    inPlan: inPlan,
                    day: t
                      .format("yyyy-MM-DD kk:mm:ss")
                      .replace(/ 24\:/, " 00:"),
                  })
                );
                window.location.reload();
              }
            })
            .catch((error) => {
              if (error.response.status === 400) {
                console.log(error.response);
              }
            });
        } else {
          ElMessage({
            type: "error",
            message: "You currently have not completed this plan.",
            center: true,
          });
        }
      });
    };
    // ---------   tools   ---------- //
    const rescale = () => {
      map.value.fitBounds(bounds.value);
      map.value.setCenter(bounds.value.getCenter());
    };
    const reset = () => {
      ElMessageBox.confirm("All data will be reset!", "Warning", {
        confirmButtonText: "Confirm",
        cancelButtonText: "Cancel",
        type: "warning",
      })
        .then(() => {
          if (directionsRenderer.value) {
            directionsRenderer.value.setMap(null);
            directionsRenderer.value = null;
          }
          for (let s in marker_start) {
            marker_start[s].setMap(null);
          }
          for (let p in marker_properties) {
            marker_properties[p].setMap(null);
          }
          init();
          inPlan.start = null;
          inPlan.places = [];
          inPlan.time = null;
          lastAddrBuffer.current = { loc: null, formatted_address: null };
          lastAddrBuffer.prefer = null;
          lastAddrBuffer.manual = null;
        })
        .catch(() => {});
    };
    const routeScale = () => {
      if (directionsRenderer.value) {
        directionsRenderer.value.setMap(null);
        directionsRenderer.value.setMap(map.value);
      }
    };
    const Cancel = () => {
      ElMessageBox.confirm("The form will be lost!", "Warning", {
        confirmButtonText: "Confirm",
        cancelButtonText: "Cancel",
        type: "warning",
      }).then(() => {
        window.location.reload();
      });
    };
    watch(
      () => inPlan.start,
      (newVal, oldVal) => {
        changeStart(newVal);
      }
    );
    watch(
      () => inPlan.places,
      (newVal, oldVal) => {
        changePlace(newVal);
      }
    );
    watch(
      inPlan,
      (newVal, oldVal) => {
        if (directionsRenderer.value) {
          directionsRenderer.value.setMap(null);
          directionsRenderer.value = null;
        }
        planRoute();
      },
      { deep: true }
    );
    return {
      // maps
      map,
      bounds,
      init,
      directionsRenderer,
      setBounds,
      // places
      addr,
      startMode,
      changeStartMode,
      getGeo,
      refreshCurrent,
      lastAddrBuffer,
      freshCurrentLoading,
      // markers
      marker_manual,
      marker_start,
      marker_properties,
      setStartMarker,
      // plan
      plan,
      inPlan,
      generateRoute,
      getManual,
      clearManual,
      plan_result,
      planRoute,
      submitPlan,
      // map tools
      rescale,
      reset,
      routeScale,
      // utils
      dialogVisible,
      changeStart,
      changePlace,
      changeTime,
      DTPicker,
      timeAlert,
      Cancel,
      completeAlert,
    };
  },
});
</script>

<style scoped>
.scale-tools {
  background-color: #ffffff;
  border: solid 3px #000000;
  border-radius: 2px;
  margin: 10px;
  padding: 3px;
  font: 400 18px Roboto, Arial, sans-serif;
  width: 100px;
}

.legend {
  background-color: #ffffff;
  border: solid 3px #000000;
  margin: 10px;
  padding: 0 0.5em;
  font: 200 16px Roboto, Arial, sans-serif;
}
</style>
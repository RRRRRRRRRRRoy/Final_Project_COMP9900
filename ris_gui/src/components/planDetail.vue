<template>
  <div>
    <el-row>
      <el-card style="width: 500px; background-color: white" shadow="never"
        ><el-scrollbar height="71vh">
          <el-timeline>
            <el-timeline-item
              v-for="(contents, index) in timelines"
              :key="index"
              placement="top"
              center
              size="large"
            >
              <el-card style="border-radius: 10px; border: 3px solid black"
                ><el-row justify="space-between"
                  ><div>
                    <div class="location-circle" v-if="index % 2">
                      {{ letters[(index + 1) / 2] }}
                    </div>
                    <el-row v-if="index % 2 === 0" align="middle">
                      <div v-if="index === 0" class="location-circle">
                        {{ letters[legs.length] }}
                      </div>
                      <div v-else class="location-circle">
                        {{ letters[index / 2] }}
                      </div>
                      <i
                        class="el-icon-arrow-right"
                        style="color: red; font-weight: bold"
                      />
                      <div class="location-circle">
                        {{ letters[index / 2 + 1] }}
                      </div>
                    </el-row>
                  </div>
                  <span style="font-weight: bold; font-size: 25px">
                    {{ contents.keywords }}</span
                  ></el-row
                ><span style="font-size: 20px; font-weight: bold">
                  {{ contents.time.replace(/^24\:/, "00:") }}</span
                >&nbsp; &nbsp; &nbsp; &nbsp;<span
                  style="font-size: 15px; font-weight: bold"
                >
                  {{ contents.date }}</span
                >
                <div style="font-size: 18px; font-weight: bold">
                  {{ contents.content }}
                </div></el-card
              >
            </el-timeline-item>
          </el-timeline></el-scrollbar
        >
      </el-card>
      <div id="detail-resacle" class="scale-tools">
        <el-button type="primary" @click="routeScale" circle icon="el-icon-refresh" />
      </div>
      <div id="plan-map" style="width: 50vw; height: 71vh; border-radius: 5px"
    /></el-row>
  </div>
</template>


<script>
import { defineComponent, onMounted, ref } from "vue";
import moment from "moment";
export default defineComponent({
  setup() {
    const map = ref(null);
    const route = ref(null);
    const renderer = ref(null);
    const duration = ref(0);
    const startTime = ref(null);
    const timelines = ref(null);
    const legs = ref(null);
    const letters = "ABCDEFGH";
    const routeScale = () => {
      if (renderer.value) {
        renderer.value.setMap(null);
        renderer.value.setMap(map.value);
      }
    };
    onMounted(() => {
      let scale_tools = document.getElementById("detail-resacle");
      map.value = new google.maps.Map(document.getElementById("plan-map"), {
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
      renderer.value = new google.maps.DirectionsRenderer({
        map: map.value,
        markerOptions: { optimized: true },
      });
      route.value = JSON.parse(localStorage.getItem("plan"));
      renderer.value.setDirections(route.value.plan);
      if (!("overview_path" in route.value.plan.routes[0])) {
        new google.maps.Polyline({
          path: google.maps.geometry.encoding.decodePath(
            route.value.plan.routes[0].overview_polyline.points
          ),
          geodesic: true,
          map: map.value,
          strokeColor: "#1E90FF",
          strokeOpacity: 0.7,
          strokeWeight: 4,
        });
      }
      duration.value = route.value.duration;
      startTime.value = new moment(route.value.day);
      legs.value = route.value.plan.routes[0].legs;
      let procedure = new Array();
      for (let i in legs.value) {
        let contents = {
          time: startTime.value.format("kk:mm:ss"),
          date: startTime.value.format("ddd, yyyy-MM-DD"),
          keywords: `${legs.value[i].distance.text}, ${legs.value[i].duration.text}`,
          content: null,
        };
        if (Number(i) === 0) {
          contents.content = `Start at ${legs.value[i].start_address.replace(
            ", Australia",
            ""
          )}, driving to the first property.`;
        } else if (Number(i) === legs.value.length - 1) {
          startTime.value.add(duration.value, "m");
          contents.time = startTime.value.format("kk:mm:ss");
          contents.date = startTime.value.format("ddd, yyyy-MM-DD");
          contents.content = `Driving back to your start location.`;
        } else {
          startTime.value.add(duration.value, "m");
          contents.time = startTime.value.format("kk:mm:ss");
          contents.date = startTime.value.format("ddd, yyyy-MM-DD");
          contents.content = `Driving to next property.`;
        }
        procedure.push(contents);
        startTime.value.add(legs.value[i].duration.value, "s");
        if (Number(i) < legs.value.length - 1) {
          let contents = {
            time: startTime.value.format("kk:mm:ss"),
            date: startTime.value.format("ddd, yyyy-MM-DD"),
            keywords: `${duration.value} mins`,
            content: null,
          };
          contents.content = `Inspect at ${legs.value[i].end_address.replace(
            ", Australia",
            ""
          )}.`;
          procedure.push(contents);
        } else {
          let contents = {
            time: startTime.value.format("kk:mm:ss"),
            date: startTime.value.format("ddd, yyyy-MM-DD"),
            keywords: "",
            content: null,
          };
          contents.content = `Arrive at start location, ${legs.value[
            i
          ].end_address.replace(", Australia", "")}.`;
          procedure.push(contents);
        }
      }
      timelines.value = procedure;
    });
    return {
      map,
      letters,
      route,
      renderer,
      duration,
      startTime,
      timelines,
      legs,
      routeScale,
    };
  },
});
</script>

<style scoped>
.location-circle {
  font-family: Arial, Helvetica, sans-serif;
  color: white;
  background-color: firebrick;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  text-align: center;
  line-height: 30px;
}

.scale-tools {
  margin: 10px;
  font: 400 18px Roboto, Arial, sans-serif;
}
</style>
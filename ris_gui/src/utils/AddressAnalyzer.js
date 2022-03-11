import axios from 'axios';


function AddressAnalyzer(address){ 
    // const address = "121-125%20Bland%20street%20Ashfield"
    const new_address = address.replace(/\s/g,"%20");
    const GoogleMapKey = 'AIzaSyDb8WLdQ91JzeQwG9BJVVJ2L9bCo0V8ZCc';
    axios.get(
        `https://maps.googleapis.com/maps/api/geocode/json?address=${new_address}&key=${GoogleMapKey}`,{})
        .then(function (response) {
        // var time = (new Date()).getTime();//获取当前的unix时间戳
        // while((new Date()).getTime() - time > 5000){
        //     console.log('3')
        // }
        if(response.status == 200) {
            // var result = response.data.result;
            // var time = (new Date()).getTime();//获取当前的unix时间戳
            // while((new Date()).getTime() - time > 3){
            //     console.log('3')
            // }
            window.lat_lng = response.data.results[0].geometry.location;
            localStorage.setItem("lat", response.data.results[0].geometry.location.lat);
            localStorage.setItem("lng", response.data.results[0].geometry.location.lng);
            // return lng_lat
            // return {latitude, longitude}
            // console.log("type of lat_lng ", typeof lat_lng)
            // console.log("This is response: ", response)
            // console.log("This is returned lat",lat_lng.lat)
            // console.log("This is returned lng",lat_lng.lng)
        }
    })
    
}
export default AddressAnalyzer;

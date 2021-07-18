// Stores list of visualization recommendations
var visList = [];

// Stores list of visualization recommendations
var vis_history_List = [];

var vis_recommend_history_List=[];

var feedback = "init_feedback";

var query_history_list=[]

var is_click=false

var task_Now=[]

var task_Next=[]
// oldNewAmbiguousAttribute
var oldNewAmbiguousAttribute = {};

// oldNewAmbiguousValues
var oldNewAmbiguousValues = {};

// Data to QueryPhrase Mapping
var dataQueryPhraseMapping = {};

// QueryPhrase to Attribute Mapping
var queryPhraseToAttrMapping = {};

// Attribute to Data Mapping
var attrToDataMapping = {};

// List of attribute ambiguities
var attributeAmbiguityList = [];

// List of value ambiguities
var valueAmbiguityList = [];

// The AttributeMap: Response from NL4DV
var attributeMap = {};

function emptyDatasetContainers(){
    $(globalConfig.extractedMetaDataContainer + " table tbody").empty();
}

function emptyQueryResponseContainers(){
    // Variables
    visList = [];
    oldNewAmbiguousValues = {};
    oldNewAmbiguousAttribute = {};
    attrToDataMapping = {};
    queryPhraseToAttrMapping = {};
    dataQueryPhraseMapping = {};
    attributeAmbiguityList = [];
    valueAmbiguityList = [];
    attributeMap = {};

    // Generated Ambiguity Dropdowns and the Formattted Query
    // document.getElementById("inputQueryContainer").innerHTML = "No query executed!"

    // VIS
    $(globalConfig.visContainer).empty();
}

function processDataResponse(response, dataset){
    emptyDatasetContainers();

    // container for Extracted Meta  Data
    $("#datasetUrl").text(dataset);
    $("#columnCount").text(response['columnCount']);
    $("#rowCount").text(response['rowCount']);

    Object.keys(response['summary']).forEach(function(attr){
        var row = document.createElement('tr');

        var cell_attribute = document.createElement('td');
        $(cell_attribute).addClass("text-no-wrap");
        $(cell_attribute).text(attr);
        $(row).append(cell_attribute);

        var domain = JSON.stringify(response['summary'][attr]['summary']);
        var dataType = response['summary'][attr]['dataType'];

        var cell_domain = document.createElement('td');
        $(cell_domain).addClass("text-no-wrap");
        if(dataType == "Q"){
            $(cell_domain).text(response['summary'][attr]['summary']["min"] + "-" + response['summary'][attr]['summary']["max"]);
        }else if(dataType == "T"){
            var start = (new Date(response['summary'][attr]['summary']["start"])).getFullYear();
            var end = (new Date(response['summary'][attr]['summary']["end"])).getFullYear();
            $(cell_domain).text(start + "-" + end);
        }else{
            $(cell_domain).text(Object.keys(response['summary'][attr]['summary']["group_counts"]).slice(1, 3) + " ...");
        }

        $(row).append(cell_domain);

        $(globalConfig.extractedMetaDataContainer + " table tbody").append(row);
    });
}
  // var query_find_extremum="Which year has the largest gdp in US?"
  // var query_trend="What is the trend of GDP over the years in US?"
  // var query_find_value="what is the value of GDP in 2019 in US?"
  // var query_find_correlation="what is relation among GDP, Service, Architecture and Industry ?"
  // var query_find_difference="what is the difference among GDP, Service and Architecture after 2015 in US?"
  // var query_find_distribution = "what is the distribution of GDP, Service and Architecture over the years in US?"
  // var query_find_rank = "what is the order of GDP after 2015 in US?"
  // var query_find_proportion = "what is the proportion of Service in GDP after 2015 in US?"
  // var query_find_aggregation="what is the average of GDP between 2015 and 2019?"
  var query_find_extremum1="Which year has the largest gdp?"
  var query_trend1="What is the trend of GDP over the years?"
  var query_find_value1="what is the value of GDP in 2019 in?"
  var query_find_correlation1="what is relation among GDP, Service, Architecture and Industry ?"
  var query_find_difference1="what is the difference among GDP, Service and Architecture after 2015?"
  var query_find_distribution1 = "what is the distribution of GDP, Service and Architecture over the years?"
  var query_find_rank1 = "what is the order of GDP after 2015?"
  var query_find_proportion1 = "what is the proportion of Service in GDP after 2015?"
  var query_find_aggregation1="what is the average of GDP between 2015 and 2019?"
  var Query=[
         query_find_proportion1, query_find_distribution1, query_find_aggregation1, query_find_difference1, query_find_rank1,
         query_trend1, query_find_correlation1, query_find_value1, query_find_extremum1]
$(globalConfig.testBtn).on("click",function () {
        var dataset = "economic.csv";
        for(var i=0;i<Query.length;i++){
            var query =Query[i];
            document.getElementById("outputVisContainer").innerHTML="";
    document.getElementById("visThumbnailContainer").innerHTML="";
    // $("#vis").remove()
    // print(query)
    // print(dataset)
            $.ajaxSettings.cache=false
            $.ajaxSettings.asymp=false
            $.ajaxSettings.async=false
    $.post("/vis", {"query": query,"table_path":dataset})
        .done(function (response) {
            var Option = JSON.parse(response);
            // $.ajax({
            // cache: false, //关闭AJAX相应的缓存
            //      asymp: false,
            //     async:false
            // });
            vis_history_List.push(Option)
            query_history(vis_history_List)
            for(var i=0;i<Option['option'].length;i++) {
                if (i == 0) {
                    $("#outputVisContainer").removeAttr("_echarts_instance_").empty();
                    var main_vis = echarts.init(document.getElementById("outputVisContainer"), 'white', {renderer: 'svg'})
                    main_vis.setOption(Option['option'][i])
                }
                var thumbnail = document.createElement("div");
                var divId = document.createAttribute("id"); //创建id
                divId.value="visThumbnail-" + i.toString();
                thumbnail.setAttributeNode(divId)
                // thumbnail.id = "visThumbnail-" + i.toString();
                var ID=thumbnail.id;
                if (i != 0) {
                    thumbnail.className = "thumbnail";
                } else {
                    thumbnail.className = "thumbnail thumbnail-active";
                }
                thumbnail.addEventListener("click", function () {
                    $(this).parent().find(".thumbnail").removeClass("thumbnail-active");
                    $(this).addClass("thumbnail-active");
                    var index = parseInt(this.id.split("-")[1]);
                    document.getElementById("outputVisContainer").innerHTML="";
                    $("#outputVisContainer").removeAttr("_echarts_instance_").empty();
                    var main_vis = echarts.init(document.getElementById("outputVisContainer"), 'white', {renderer: 'svg'});
                    console.log(main_vis)
                    main_vis.setOption(Option['option'][index]);
                })
                document.getElementById('visThumbnailContainer').appendChild(thumbnail);
                var add_vis = echarts.init(document.getElementById("visThumbnail-" + i.toString()),'white',{renderer:'svg'});
                add_vis.setOption(Option['option'][i]);
                var IDD="visThumbnail-" + i.toString()
                d3.select("#"+IDD).selectAll('div').selectAll('svg').selectAll('g').selectAll('text').style("font-size","9px")
                    // document.getElementById('isThumbnailContainer').appendChild(thumbnail);
            }
        });
            $.ajaxSettings.async=true
        }

})
function unique1(arr){
  var hash=[];
  for (var i = 0; i < arr.length; i++) {
     if(hash.indexOf(arr[i])==-1){
      hash.push(arr[i]);
     }
  }
  return hash;
}
$(globalConfig.queryBtn).on("click",function () {
    var query = $(globalConfig.queryInput).val();
    var dataset = $(globalConfig.datasetSelect).val();
    document.getElementById("outputVisContainer").innerHTML="";
    document.getElementById("visThumbnailContainer").innerHTML="";
    document.getElementById("re_0").innerHTML="";
    document.getElementById("re_1").innerHTML="";
    document.getElementById("re_2").innerHTML="";
    document.getElementById("re_3").innerHTML="";
    if(is_click==false){
        if(feedback!="init_feedback"){
            feedback=""
            feedback=feedback+"negative_feedback"+"-"+task_Now[0]+"-"+task_Next[0]+"-"+task_Next[1]
        }
    }
    // $("#vis").remove()
    // print(query)
    // print(dataset)
    $.post("/vis", {"query": query,"table_path":dataset,"Feedback":feedback,})
        .done(function (response) {
            var result= JSON.parse(response);
            var Option = result['option'];
            var vis_recommend=result['recommend'];
            var task_now=result['task']
            task_Now.push(task_now)
            for(var i=0;i<vis_recommend.length;i++){
                task_Next.push(vis_recommend[i][0])
            }
            task_Next=unique1(task_Next)

            console.log("vis_recommend")
            console.log(vis_recommend)
            $.ajax({
            cache: false, //关闭AJAX相应的缓存
                 asymp: false
            });
            for(var i=0;i<4;i++){
                var re=$("#"+"re_"+i.toString())
                re.unbind("click")
            }
            // vis_history_List.push(Option)
            // vis_recommend_history_List.push(vis_recommend)
            query_history_list.push(result)
            query_history(query_history_list)
            query_recommend(vis_recommend,task_now)
            is_click=false
            for(var i=0;i<Option['option'].length;i++) {
                if (i == 0) {
                    $("#outputVisContainer").removeAttr("_echarts_instance_").empty();
                    var main_vis = echarts.init(document.getElementById("outputVisContainer"), 'white', {renderer: 'svg'})
                    main_vis.setOption(Option['option'][i])
                }
                var thumbnail = document.createElement("div");
                var divId = document.createAttribute("id"); //创建id
                divId.value="visThumbnail-" + i.toString();
                thumbnail.setAttributeNode(divId)
                // thumbnail.id = "visThumbnail-" + i.toString();
                var ID=thumbnail.id;
                if (i != 0) {
                    thumbnail.className = "thumbnail";
                } else {
                    thumbnail.className = "thumbnail thumbnail-active";
                }
                thumbnail.addEventListener("click", function () {
                    $(this).parent().find(".thumbnail").removeClass("thumbnail-active");
                    $(this).addClass("thumbnail-active");
                    var index = parseInt(this.id.split("-")[1]);
                    document.getElementById("outputVisContainer").innerHTML="";
                    $("#outputVisContainer").removeAttr("_echarts_instance_").empty();
                    var main_vis = echarts.init(document.getElementById("outputVisContainer"), 'white', {renderer: 'svg'});
                    console.log(main_vis)
                    main_vis.setOption(Option['option'][index]);
                })
                document.getElementById('visThumbnailContainer').appendChild(thumbnail);
                var add_vis = echarts.init(document.getElementById("visThumbnail-" + i.toString()),'white',{renderer:'svg'});
                add_vis.setOption(Option['option'][i]);
                var IDD="visThumbnail-" + i.toString()
                d3.select("#"+IDD).selectAll('div').selectAll('svg').selectAll('g').selectAll('text').style("font-size","9px")
                    // document.getElementById('isThumbnailContainer').appendChild(thumbnail);
            }
        });
})
function query_recommend(vis_recommend,task_now){
    document.getElementById("re_0").innerHTML="";
    document.getElementById("re_1").innerHTML="";
    document.getElementById("re_2").innerHTML="";
    document.getElementById("re_3").innerHTML="";
    for(var i=0;i<vis_recommend.length;i++){
        // var main_vis = echarts.init(document.getElementById("re_"+i.toString()), 'white', {renderer: 'svg'})
        // main_vis.setOption(vis_recommend[i]['option']['option'][0])
        var query=vis_recommend[i][1]
        var task_next=vis_recommend[i][0]
        var Img=document.createElement("img")
        Img.src="../static/img/symbol/"+task_next+".png"
        Img.setAttribute("class","flag")
        var span = document.createElement("span");
        span.setAttribute("class","flag_text")
        span.innerText=query
        // var recommend = document.getElementById("re_"+i.toString());
        // recommend.appendChild(Img)
        // recommend.appendChild(span)
        // recommend.addEventListener("click",Add)
        // function Add () {
        //     var index = parseInt(this.id.split("_")[1]);
        //     var Query = vis_recommend[index][1];
        //     re_input(Query)
        //     console.log(Query)
        //     console.log("------")
        //     add_task(task_now,task_next)
        //     is_click=true
        //     $(globalConfig.queryBtn).trigger("click")
        // }
        var recommend=$("#"+"re_"+i.toString());
        recommend.append(Img)
        recommend.append(span)
        recommend.bind("click",function () {
            var index = parseInt(this.id.split("_")[1]);
            var Query = vis_recommend[index][1];
            re_input(Query)
            console.log(Query)
            console.log("------")
            add_task(task_now,task_next)
            is_click=true
            $(globalConfig.queryBtn).trigger("click")
        })
        d3.select("#re_"+i.toString()).selectAll('div').selectAll('svg').selectAll('g').selectAll('text').style("font-size","9px")
    }
}
function add_task(task_now,task_next) {
    // feedback.push(task_now)
    // feedback.push(task_next)
    feedback=""
    feedback=feedback+"positive_feedback"+"-"+task_now+"-"+task_next
}
function re_input(value) {
    $(globalConfig.queryInput).val(value).trigger('input',value)
    $(globalConfig.queryInput).val(value)
}
function configureDatabase(dataset){
    $.post("/setData", {"dataset": dataset})
        .done(function (response) {
            var attributeTypeChanges = {};
            var ignore_words = [];
            if(dataset == "cars-w-year.csv"){
                attributeTypeChanges = {
                    "Year": "T"
                };
                ignore_words = ['car'];
            }else if(dataset == "cars.csv"){
                ignore_words = ['car'];
            }else if(dataset == "movies-w-year.csv"){
                attributeTypeChanges = {
                    "Release Year": "T"
                };
                ignore_words = ['movie'];
            }else if(dataset == "housing.csv"){
                attributeTypeChanges = {
                    "Year": "T"
                }
                ignore_words = [];
            }else if(dataset == "olympic_medals.csv"){
                attributeTypeChanges = {
                    "Gold Medal": 'Q',
                    "Silver Medal": 'Q',
                    "Bronze Medal": 'Q',
                    "Total Medal": 'Q',
                    "Year": "T"
                }
                ignore_words = [];
            }

            if(attributeTypeChanges != {}){
                $.post("/setAttributeDataType", {"attr_type_obj": JSON.stringify(attributeTypeChanges)})
                    .done(function (r2) {
                        processDataResponse(r2, dataset);
                    });
            }

            if(ignore_words.length > 0){
                $.post("/setIgnoreList", {"ignore_words": JSON.stringify(ignore_words)})
                    .done(function (r3) {
                    });
            }

            if(attributeTypeChanges == {} && ignore_words.length == 0){
                processDataResponse(r1, dataset);
            }

        });
}
$(document).ready(function(){
    var Querysent = $(globalConfig.queryInput).val();
    $('#queryInput').autocomplete({
   source:function(query,process){
       console.log(query)
       var Dataset=$(globalConfig.datasetSelect).val();
      $.post("/input_association",{"Querysent":query.term,"Dataset":Dataset},function(respData){
           respData =JSON.parse(respData);//解析返回的数据
           return process(respData['association']);
       });
    },
        messages: {
        noResults: '',
        results: function() {}
    }
});
});
function query_history(query_history_list){
    var zb=document.getElementById("carousel-indicators")
    var xm=document.getElementById("carousel-inner")
    zb.innerHTML=""
    xm.innerHTML=""
    console.log(vis_history_List)
    console.log(vis_history_List.length)
    if(query_history_list.length!=0){
        for(var i=0;i<query_history_list.length;i++){

            if(i==0){
                var ol=document.getElementById("carousel-indicators");
                var li=document.createElement("li");
                li.setAttribute("data-target","#myCarousel");
                li.setAttribute("data-slide-to",i.toString());
                li.setAttribute("class","active");
                ol.appendChild(li)
                var target=document.getElementById("carousel-inner")
                var vis=document.createElement("div")
                var obj=document.createElement("div")
                var obj_1=document.createElement("div")
                vis.setAttribute("id","vis_history-"+i.toString())
                vis.setAttribute("class","history")
                vis.addEventListener("click",function () {
                    var index = parseInt(this.id.split("-")[1]);
                    re_vis(query_history_list[index]['option'])
                    re_recommend_vis(query_history_list[index]['recommend'],query_history_list[index]['task'])
                })
                obj.setAttribute("class","item active")
                obj_1.setAttribute("class","carousel-caption")
                obj_1.innerHTML= '<span style="color: '+"black"+'">' +"Question: "+(i+1).toString()+ " </span>";
                obj.appendChild(vis)
                obj.appendChild(obj_1)
                target.appendChild(obj)
                var add_vis = echarts.init(document.getElementById("vis_history-" + i.toString()),'white',{renderer:'svg'});
                add_vis.setOption(query_history_list[i]['option']['option'][0]);

            }
            else {
                var ol=document.getElementById("carousel-indicators")
                var li=document.createElement("li")
                li.setAttribute("data-target","#myCarousel");
                li.setAttribute("data-slide-to",i.toString());
                ol.appendChild(li)
                var target=document.getElementById("carousel-inner")
                var vis=document.createElement("div")
                var obj=document.createElement("div")
                var obj_1=document.createElement("div")
                vis.setAttribute("id","vis_history-"+i.toString())
                vis.setAttribute("class","history")
                vis.addEventListener("click",function () {
                    var index = parseInt(this.id.split("-")[1]);
                    re_vis(query_history_list[index]['option'])
                    re_recommend_vis(query_history_list[index]['recommend'])
                    console.log("调用history")
                })
                obj.setAttribute("class","item")
                obj_1.setAttribute("class","carousel-caption")
                obj_1.innerHTML= '<span style="color: '+"black"+'">' +"Question: "+(i+1).toString()+ " </span>";
                obj.appendChild(vis)
                obj.appendChild(obj_1)
                target.appendChild(obj)
                var add_vis = echarts.init(document.getElementById("vis_history-" + i.toString()),'white',{renderer:'svg'});
                add_vis.setOption(query_history_list[i]['option']['option'][0]);
            }

        }
    }
};
$(globalConfig.datasetSelect).change(function() {
    emptyQueryResponseContainers();
    emptyDatasetContainers();
    var dataset = $(this).val();
    console.log("111111111111")
    console.log(dataset)
    if(dataset=="bill.csv")
    {$(globalConfig.queryInput).val("what is the mean of cost?")}
    else if(dataset=="Cars-w-year.csv")
    {$(globalConfig.queryInput).val("what is the distribution of Horsepower?")}
    else if(dataset=="colleges.csv")
    {$(globalConfig.queryInput).val("what is the distribution of SATAverage?")}
    else if(dataset=="happiness.csv")
    {$(globalConfig.queryInput).val("what is the distribution of HappinessScore?")}
    else if(dataset=="Movies-w-year.csv")
    {$(globalConfig.queryInput).val("what is the distribution of IMDBRating?")}
    configureDatabase(dataset);
});
function re_recommend_vis(vis_recommend,task_now) {
    document.getElementById("re_0").innerHTML="";
    document.getElementById("re_1").innerHTML="";
    document.getElementById("re_2").innerHTML="";
    document.getElementById("re_3").innerHTML="";
    for(var i=0;i<4;i++){
                var re=$("#"+"re_"+i.toString())
                re.unbind("click")
    }
    for(var i=0;i<vis_recommend.length;i++){
        // var main_vis = echarts.init(document.getElementById("re_"+i.toString()), 'white', {renderer: 'svg'})
        // main_vis.setOption(vis_recommend[i]['option']['option'][0])
        var query=vis_recommend[i][1]
        var task_next=vis_recommend[i][0]
        var Img=document.createElement("img")
        Img.src="../static/img/symbol/"+task_next+".png"
        Img.setAttribute("class","flag")
        var span = document.createElement("span");
        span.setAttribute("class","flag_text")
        span.innerText=query
        var recommend=$("#"+"re_"+i.toString());
        recommend.append(Img)
        recommend.append(span)
        recommend.bind("click",function () {
            var index = parseInt(this.id.split("_")[1]);
            var Query = vis_recommend[index][1];
            re_input(Query)
            console.log(Query)
            console.log("------")
            add_task(task_now,task_next)
            is_click=true
            $(globalConfig.queryBtn).trigger("click")
        })
        d3.select("#re_"+i.toString()).selectAll('div').selectAll('svg').selectAll('g').selectAll('text').style("font-size","9px")
    }
}

function re_vis(Option) {
        document.getElementById("outputVisContainer").innerHTML="";
       document.getElementById("visThumbnailContainer").innerHTML="";
       for(var i=0;i<Option['option'].length;i++) {
                if (i == 0) {
                    $("#outputVisContainer").removeAttr("_echarts_instance_").empty();
                    var main_vis = echarts.init(document.getElementById("outputVisContainer"), 'white', {renderer: 'svg'})
                    main_vis.setOption(Option['option'][i])
                }
                var thumbnail = document.createElement("div");
                var divId = document.createAttribute("id"); //创建id
                divId.value="visThumbnail-" + i.toString();
                thumbnail.setAttributeNode(divId)
                // thumbnail.id = "visThumbnail-" + i.toString();
                var ID=thumbnail.id;
                if (i != 0) {
                    thumbnail.className = "thumbnail";
                } else {
                    thumbnail.className = "thumbnail thumbnail-active";
                }
                thumbnail.addEventListener("click", function () {
                    $(this).parent().find(".thumbnail").removeClass("thumbnail-active");
                    $(this).addClass("thumbnail-active");
                    var index = parseInt(this.id.split("-")[1]);
                    document.getElementById("outputVisContainer").innerHTML="";
                    $("#outputVisContainer").removeAttr("_echarts_instance_").empty();
                    var main_vis = echarts.init(document.getElementById("outputVisContainer"), 'white', {renderer: 'svg'});
                    console.log(main_vis)
                    main_vis.setOption(Option['option'][index]);
                })
                document.getElementById('visThumbnailContainer').appendChild(thumbnail);
                var add_vis = echarts.init(document.getElementById("visThumbnail-" + i.toString()),'white',{renderer:'svg'});
                add_vis.setOption(Option['option'][i]);
                var IDD="visThumbnail-" + i.toString()
                d3.select("#"+IDD).selectAll('div').selectAll('svg').selectAll('g').selectAll('text').style("font-size","9px")
                    // document.getElementById('isThumbnailContainer').appendChild(thumbnail);
            }
}
function getVisSpec(){
    var currSelections = [];
    Object.keys(oldNewAmbiguousValues).forEach(function(item){
       currSelections.push(oldNewAmbiguousValues[item]["new"]);
    });

    for(var i=0; i < visList.length; i++){

        // We just want BAR CHART to recreate DataTone
        if (visList[i]["vlSpec"]["mark"]["type"] != "bar"){
            continue
        }

        var is_x = "x" in visList[i]["vlSpec"]["encoding"];
        var is_y = "y" in visList[i]["vlSpec"]["encoding"];
        var is_c = "color" in visList[i]["vlSpec"]["encoding"];
        var is_s = "size" in visList[i]["vlSpec"]["encoding"];

        var x = null, y = null, c = null, s = null;

        if(is_x){
            x = visList[i]["vlSpec"]["encoding"]["x"]["field"];
            visList[i]["vlSpec"]["encoding"]["x"]["axis"] = {"labelFontSize": 14, "titleFontSize": 16, "titlePadding": 16}
        }
        if(is_y){
            y = visList[i]["vlSpec"]["encoding"]["y"]["field"];
            visList[i]["vlSpec"]["encoding"]["y"]["axis"] = {"labelFontSize": 14, "titleFontSize": 16, "titlePadding": 16}
        }
        if(is_c){
            c = visList[i]["vlSpec"]["encoding"]["color"]["field"];
        }
        if(is_s){
            s = visList[i]["vlSpec"]["encoding"]["size"]["field"];
        }

        if((x!= null && currSelections.indexOf(x) === -1) || (y!=null &&  currSelections.indexOf(y) === -1) || (c!=null && currSelections.indexOf(c) === -1) || (s!=null && currSelections.indexOf(s) === -1)){
            // console.log(x, y, c);
            continue;
        }
        if(is_x && x in attrToDataMapping){
            visList[i]["vlSpec"]["encoding"]["x"]["field"] = oldNewAmbiguousValues[attrToDataMapping[x]]["new"];
        }
        if(is_y && y in attrToDataMapping){
            visList[i]["vlSpec"]["encoding"]["y"]["field"] = oldNewAmbiguousValues[attrToDataMapping[y]]["new"];
        }
        if(is_c && c in attrToDataMapping){
            visList[i]["vlSpec"]["encoding"]["color"]["field"] = oldNewAmbiguousValues[attrToDataMapping[c]]["new"];
        }
        if(is_s && s in attrToDataMapping){
            visList[i]["vlSpec"]["encoding"]["size"]["field"] = oldNewAmbiguousValues[attrToDataMapping[s]]["new"];
        }

        var chartTitle = [];
        // MODIFY FILTER VALUE LEVEL AMBIGUITY
        visList[i]["vlSpec"]["transform"].forEach(function(transformObj){
            var _item = transformObj["filter"]["field"];
            var clickedItems = oldNewAmbiguousAttribute[_item]["new"];
            if("filter" in transformObj){
                if(transformObj["filter"]["field"] == _item){
                    clickedItems.forEach(function(clickedItem){
                        attributeMap[_item]["meta"]["ambiguity"][dataQueryPhraseMapping[clickedItem]].forEach(function(to_remove){
                            var index = transformObj["filter"]["oneOf"].indexOf(to_remove);
                            if (index !== -1) transformObj["filter"]["oneOf"].splice(index, 1);
                        });
                        transformObj["filter"]["oneOf"].push(clickedItem);
                    });
                    chartTitle.push(_item + " = " + transformObj["filter"]["oneOf"].toString());
                }
            }
        });

        // Add FILTERS in the chart title
        visList[i]["vlSpec"]["title"] = {
          "text": chartTitle.join(" | "),
          "align": "right",
          "orient": "top",
          "fontSize": 14,
          "color": "gray",
          "fontWeight": "light",
          "anchor": "end"
        }

        break
    }

    return visList[i];
}

function updateViz(spec){
    if(spec != null){
        if(JSON.stringify(spec["vlSpec"]['encoding']) != "{}"){
            var visDiv = document.getElementById('datatone-viz');
            spec["vlSpec"]["width"] = 500;
            spec["vlSpec"]["height"] = 300;
            vegaEmbed(visDiv, spec["vlSpec"], vegaOptMode);
        }
    }
}

function updateJSONTree(spec){
    if(spec != null){
        var divSpec = document.getElementById('datatone-spec');
        var tree = jsonTree.create(spec, divSpec);
        tree.expand();
    }
}
function initialize(){
var dataset = $(globalConfig.datasetSelect).val();
    $.post("/init", {"dependency_parser": "corenlp"})
        .done(function (response) {
            configureDatabase(dataset);
        });
}
$(document).ready(function() {
    initialize();
    $(globalConfig.queryInput).val("what is the mean of cost?");

});

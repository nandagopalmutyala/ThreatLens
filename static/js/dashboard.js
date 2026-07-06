// ===============================
// Sidebar Toggle
// ===============================

const menuBtn = document.getElementById("menuToggle");

if(menuBtn){

    menuBtn.addEventListener("click",()=>{

        document.querySelector(".sidebar").classList.toggle("collapsed");

        document.querySelector(".main-content").classList.toggle("expanded");

    });

}

// ===============================
// Timeline Chart
// ===============================

const timelineChart = document.getElementById("timelineChart");

if (timelineChart) {

    new Chart(timelineChart, {

        type: "line",

        data: {

            labels: timelineLabels,

            datasets: [{

                label: "Total Threats Detected",

                data: timelineValues,

                borderColor: "#00D4FF",

                backgroundColor: "rgba(0,212,255,0.15)",

                fill: true,

                tension: 0.4,

                pointRadius: 5,

                pointHoverRadius: 7

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    labels: {

                        color: "#ffffff"

                    }

                }

            },

            scales: {

                x: {

    title: {

        display: true,

        text: "Threat Detection Sequence",

        color: "#ffffff"

    },

    ticks: {

        color: "#ffffff"

    },

    grid: {

        color: "rgba(255,255,255,0.08)"

    }

},

                y: {

                    beginAtZero: true,
                    title: {

                         display: true,

                        text: "Cumulative Threats",

                        color: "#ffffff"

                    },


                    ticks: {

                        color: "#ffffff"

                    },

                    grid: {

                        color: "rgba(255,255,255,0.08)"

                    }

                }

            }

        }

    });

}

// ===============================
// Doughnut Chart
// ===============================

const threatChart = document.getElementById("threatChart");

if(threatChart){

    new Chart(threatChart,{

        type:"doughnut",

        data:{

            labels:threatLabels,

            datasets:[{

                data:threatValues,

                backgroundColor:[

                    "#EF4444",
                    "#F59E0B",
                    "#06B6D4",
                    "#22C55E",
                    "#8B5CF6",
                    "#EC4899"

                ],

                borderWidth:0

            }]

        },

        options:{

            responsive:true,

            plugins:{

                legend:{

                    position:"bottom",

                    labels:{

                        color:"#ffffff",

                        font:{
                            size:14
                        }

                    }

                }

            }

        }

    });

}

// ===============================
// Counter Animation
// ===============================

const counters=document.querySelectorAll(".stats-card h2");

counters.forEach(counter=>{

    const target=parseInt(counter.innerText);

    let count=0;

    const speed=25;

    const update=()=>{

        if(count<target){

            count++;

            counter.innerText=count;

            setTimeout(update,speed);

        }

    }

    update();

});
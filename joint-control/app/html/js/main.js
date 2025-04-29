var application = function () {
  RobotUtils.onService(
    // ───── SUCCESS ─────
    function (Joint) {
      $("#noservice").hide();
      // show all seven panels + controls
      $("#button1, #button2, #button3, #button4, #button5, #button6, #button7, #controls").show();

      // 1) RShoulderPitch
      Joint.getJoint("RShoulderPitch").then(function (deg) {
        $("#rsp-angle-input").val(deg);
      });
      $("#btn-set1").on("click", function () {
        var deg = parseFloat($("#rsp-angle-input").val());
        Joint.setJoint("RShoulderPitch", deg).catch(console.error);
      });

      // 2) LShoulderPitch
      Joint.getJoint("LShoulderPitch").then(function (deg) {
        $("#lsp-angle-input").val(deg);
      });
      $("#btn-set2").on("click", function () {
        var deg = parseFloat($("#lsp-angle-input").val());
        Joint.setJoint("LShoulderPitch", deg).catch(console.error);
      });

      // 3) RElbowYaw
      Joint.getJoint("RElbowYaw").then(function (deg) {
        $("#rey-angle-input").val(deg);
      });
      $("#btn-set3").on("click", function () {
        var deg = parseFloat($("#rey-angle-input").val());
        Joint.setJoint("RElbowYaw", deg).catch(console.error);
      });

      // 4) RWristYaw
      Joint.getJoint("RWristYaw").then(function (deg) {
        $("#rwy-angle-input").val(deg);
      });
      $("#btn-set4").on("click", function () {
        var deg = parseFloat($("#rwy-angle-input").val());
        Joint.setJoint("RWristYaw", deg).catch(console.error);
      });

      // 5) LElbowYaw
      Joint.getJoint("LElbowYaw").then(function (deg) {
        $("#ley-angle-input").val(deg);
      });
      $("#btn-set5").on("click", function () {
        var deg = parseFloat($("#ley-angle-input").val());
        Joint.setJoint("LElbowYaw", deg).catch(console.error);
      });

      // 6) LWristYaw
      Joint.getJoint("LWristYaw").then(function (deg) {
        $("#lwy-angle-input").val(deg);
      });
      $("#btn-set6").on("click", function () {
        var deg = parseFloat($("#lwy-angle-input").val());
        Joint.setJoint("LWristYaw", deg).catch(console.error);
      });

      // 7) HeadYaw
      Joint.getJoint("HeadYaw").then(function (deg) {
        $("#hyaw-angle-input").val(deg);
      });
      $("#btn-set7").on("click", function () {
        var deg = parseFloat($("#hyaw-angle-input").val());
        Joint.setJoint("HeadYaw", deg).catch(console.error);
      });

      // Reset all joints to neutral
      $("#btn-reset").on("click", function () {
        [
          "RShoulderPitch","LShoulderPitch",
          "RElbowYaw","RWristYaw",
          "LElbowYaw","LWristYaw",
          "HeadYaw"
        ].forEach(function(j) {
          Joint.resetJoint(j).catch(console.error);
        });
      });

      // Exit app (reset + go home)
      $("#btn-exit").on("click", function () {
        Joint.stop()
          .then(function () {
            RobotUtils.onService(function (ALTabletService) {
              ALTabletService.goToHome();
            });
          })
          .catch(console.error);
      });
    },

    // ───── FAILURE ─────
    function () {
      console.error("Failed to get the service.");
      $("#noservice").show();
    }
  );
};

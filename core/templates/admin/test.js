$(document).on('click', '.btn-create-mission', function(event) {
    var dict = {};
    var rowIds = datatable.rows( { selected: true } ).ids().toArray();
    if (rowIds.length == 0){
      setToast("warning",'Vui lòng chọn app !');
      $("#closeCreated").click();
      return;
    }
    dict['idDevice'] = idDevice;
    dict['listApps'] = rowIds;
    dict['listActions'] = []
    $('.custom-checkbox-card-input:checkbox').filter(":checked").each(function () {
        switch ($(this).attr("id")) {
          case "checkboxCardProfile":
            if ($('#validationInvalidTextarea1Profile').val() == ""){
              setToast("warning",'Vui lòng nhập danh sách !');
              return;
            }
            dict['listActions'].push("Profile");
            dict['listProfile'] = $('#validationInvalidTextarea1Profile').val();
            dict['customCheckFriend'] =$('#customCheckFriend').is(":checked");
            dict['inputFriend1'] = $('#inputFriend1').val();
            dict['inputFriend2'] = $('#inputFriend2').val();
            dict['inputTimeout'] = $('#inputTimeout').val();
            break;

          case "checkboxCardFollow":
            if ($('#validationInvalidTextarea1Follow').val() == ""){
              setToast("warning",'Vui lòng nhập danh sách !');
              return;
            }
            dict['listActions'].push("Follow");
            dict['listFollow'] = $('#validationInvalidTextarea1Follow').val();
            dict['customCheckFollow'] =$('#customCheckFollow').is(":checked");
            dict['inputFollow1'] = $('#inputFollow1').val();
            dict['inputFollow2'] = $('#inputFollow2').val();
            dict['inputTimeout'] = $('#inputTimeout').val();
            break;

          case "checkboxCardPost":
            if ($('#validationInvalidTextarea1Post').val() == ""){
              setToast("warning",'Vui lòng nhập danh sách !');
              return;
            }
            dict['listActions'].push("Post");
            dict['listPost'] = $('#validationInvalidTextarea1Post').val();
            dict['customRadioLike'] =$('#customRadioLike').is(":checked");
            dict['customRadioTim'] =$('#customRadioTim').is(":checked");
            dict['customRadioThuong'] =$('#customRadioThuong').is(":checked");
            dict['customRadioHaha'] =$('#customRadioHaha').is(":checked");
            dict['customRadioWow'] =$('#customRadioWow').is(":checked");
            dict['customRadioBuon'] =$('#customRadioBuon').is(":checked");
            dict['customRadioPhan'] =$('#customRadioPhan').is(":checked");
            dict['inputPostTime1'] = $('#inputPostTime1').val();
            dict['inputPostTime2'] = $('#inputPostTime2').val();
            dict['inputPostTimes1'] = $('#inputPostTimes1').val();
            dict['inputPostTimes2'] = $('#inputPostTimes2').val();
            dict['inputPostTimeCum1'] = $('#inputPostTimeCum1').val();
            dict['inputPostTimeCum2'] = $('#inputPostTimeCum2').val();
            dict['inputTimeout'] = $('#inputTimeout').val();
            break;

          case "checkboxCardComment":
            if ($('#validationInvalidTextarea1Comment').val() == ""){
              setToast("warning",'Vui lòng nhập danh sách !');
              return;
            }

            if ($('#validationInvalidTextarea1CommentContent').val() == ""){
              setToast("warning",'Vui lòng nhập nội dung comment !');
              return;
            }

            dict['listActions'].push("Comment");
            dict['listComment'] = $('#validationInvalidTextarea1Comment').val();
            dict['validationInvalidTextarea1CommentContent'] =$('#validationInvalidTextarea1CommentContent').val();
            dict['inputComment1'] = $('#inputComment1').val();
            dict['inputComment2'] = $('#inputComment2').val();
            dict['customCheckCommentImage'] =$('#customCheckCommentImage').is(":checked");
            dict['validationInvalidTextarea1CommentContentImage'] =$('#validationInvalidTextarea1CommentContentImage').val();
            dict['inputTimeout'] = $('#inputTimeout').val();
            break;

          case "checkboxCardShare":
            if ($('#validationInvalidTextarea1Share').val() == ""){
              setToast("warning",'Vui lòng nhập danh sách !');
              return;
            }
            dict['listActions'].push("Share");
            dict['listShare'] = $('#validationInvalidTextarea1Share').val();
            dict['validationInvalidTextarea1ShareContent'] =$('#validationInvalidTextarea1ShareContent').val();
            dict['inputShare1'] = $('#inputShare1').val();
            dict['inputShare2'] = $('#inputShare2').val();
            dict['inputTimeout'] = $('#inputTimeout').val();
            break;

          case "checkboxCardNewfeed":
            dict['listActions'].push("Newfeed");
            dict['inputTime1'] = $('#inputTime1').val();
            dict['inputTime2'] = $('#inputTime2').val();
            dict['inputTimes1'] = $('#inputTimes1').val();
            dict['inputTimes2'] = $('#inputTimes2').val();
            dict['inputSleep1'] = $('#inputSleep1').val();
            dict['inputSleep2'] = $('#inputSleep2').val();
            dict['customCheckOnly'] =$('#customCheckOnly').is(":checked");
            dict['customNewfeedsLike'] =$('#customNewfeedsLike').is(":checked");
            dict['customNewfeedsComment'] =$('#customNewfeedsComment').is(":checked");
            dict['inputNewfeedsNhap'] = $('#validationInvalidTextarea1NewfeedsNhap').val();
            dict['customCheckNewfeedsCommentImage'] =$('#customCheckNewfeedsCommentImage').is(":checked");
            dict['validationInvalidTextarea1NewfeedsContentImage'] =$('#validationInvalidTextarea1NewfeedsContentImage').val();
            dict['inputTimeout'] = $('#inputTimeout').val();
            break;


          case "checkboxCardGroup":         
            if ($('#validationInvalidTextarea1Group').val() == ""){
              setToast("warning",'Vui lòng nhập danh sách !');
              return;
            }
            dict['listActions'].push("Group");
            dict['listGroup'] = $('#validationInvalidTextarea1Group').val();
            dict['inputGroupTime1'] = $('#inputGroupTime1').val();
            dict['inputGroupTime2'] = $('#inputGroupTime2').val();
            dict['inputGroupTimes1'] = $('#inputGroupTimes1').val();
            dict['inputGroupTimes2'] = $('#inputGroupTimes2').val();
            dict['inputTimeout'] = $('#inputTimeout').val();
            dict['customCheckGroup'] =$('#customCheckGroup').is(":checked");
            dict['customCheckGroupComment'] =$('#customCheckGroupComment').is(":checked");
            dict['customCheckGroupLuot'] =$('#customCheckGroupLuot').is(":checked");
            dict['customCheckGroupLike'] =$('#customCheckGroupLike').is(":checked");
            dict['validationInvalidTextarea1GroupContent'] =$('#validationInvalidTextarea1GroupContent').val();
            dict['customCheckGroupCommentImage'] =$('#customCheckGroupCommentImage').is(":checked");
            dict['validationInvalidTextarea1GroupContentImage'] =$('#validationInvalidTextarea1GroupContentImage').val();
            break;

          case "checkboxCardRandomGroup":
            if ($('#customRandomGroupComment').is(":checked") && $('#validationInvalidTextarea1RandomGroupNhap').val() == ""){
              setToast("warning",'Vui lòng nhập nội dung comment !');
              return;
            }
            if ($('#customCheckRandomGroupCommentImage').is(":checked") && $('#validationInvalidTextarea1RandomGroupContentImage').val() == ""){
              setToast("warning",'Vui lòng nhập đường dẫn hình ảnh !');
              return;
            }
            dict['listActions'].push("Random");
            dict['inputRandomGroupTime1'] = $('#inputRandomGroupTime1').val();
            dict['inputRandomGroupTime2'] = $('#inputRandomGroupTime2').val();
            dict['inputRandomGroupTimes1'] = $('#inputRandomGroupTimes1').val();
            dict['inputRandomGroupTimes2'] = $('#inputRandomGroupTimes2').val();
            dict['inputRandomGroupSleep1'] = $('#inputRandomGroupSleep1').val();
            dict['inputRandomGroupSleep2'] = $('#inputRandomGroupSleep2').val();
            dict['inputRandomGroupTotal'] = $('#inputRandomGroupTotal').val();
            dict['customRandomGroupLike'] =$('#customRandomGroupLike').is(":checked");
            dict['customRandomGroupComment'] =$('#customRandomGroupComment').is(":checked");
            dict['inputRandomGroupNhap'] = $('#validationInvalidTextarea1RandomGroupNhap').val();
            dict['customCheckRandomGroupCommentImage'] =$('#customCheckRandomGroupCommentImage').is(":checked");
            dict['validationInvalidTextarea1RandomGroupContentImage'] =$('#validationInvalidTextarea1RandomGroupContentImage').val();
            dict['inputTimeout'] = $('#inputTimeout').val();
            break;

          case "checkboxCardEarnMoney":
            dict['listActions'].push("Earn");
            dict['inputLimitAction'] = $('#inputLimitAction').val();
            dict['inputTimeout'] = $('#inputTimeout').val();
            dict['inputRandomEarnTime1'] = $('#inputRandomEarnTime1').val();
            dict['inputRandomEarnTime2'] = $('#inputRandomEarnTime2').val();
            dict['inputRandomEarnTimes1'] = $('#inputRandomEarnTimes1').val();
            dict['inputRandomEarnTimes2'] = $('#inputRandomEarnTimes2').val();
            dict['inputRandomEarnEachTime1'] = $('#inputRandomEarnEachTime1').val();
            dict['inputRandomEarnEachTime2'] = $('#inputRandomEarnEachTime2').val();
            break;

          case "checkboxCardPricingRadioEg4":
            break;
          default:
          
        };
    });
    // alert(JSON.stringify(dict));
    if (dict['listActions'].length == 0){
      setToast("warning",'Vui lòng chọn nhiệm vụ !');
      return;
    }

    var myJob = {
      name_job:JSON.stringify(dict['listActions']),
      data_job:dict
    }

    check_mission = true;
    list_Status_Mission_Current = $('td.status-mission').toArray();
    list_Name_Mission_Current = $('td.list-mission').toArray();
    for (idxAAA in list_Status_Mission_Current){
      if( $(list_Status_Mission_Current[idxAAA]).html().trim().indexOf("Running") !== -1){
        setToast("warning",'Có job đang chạy vui lòng ngừng để chạy job mới !');
        check_mission = false;
      };
    };
    
    if (check_mission == true){
      $.ajax({
          url: '../../api/job/',
          type: 'POST',
          contentType: 'application/json; charset=utf-8',
          processData: false,
          data: JSON.stringify(myJob),
          headers: { "X-CSRFToken": getCookie("csrftoken") },
          success: function(data, textStatus, xhr) {
            if (xhr.status == "200" || xhr.status == "201"){
              setToast("success",'Tạo nhiệm vụ thành công !');
              location.reload();
            } else {
              setToast("error",'Tạo nhiệm vụ thất bại !');
              document.getElementById("showMessage").style.display = "block";
            }
          }
      });
    };
    $("#closeCreated").click();
  });
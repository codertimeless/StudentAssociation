var wait = 60;

function check_input() {
    var phone_number = document.getElementById("with_code_input").value;
    var error = document.getElementById("error_block");

    if (phone_number) {
        return phone_number
    } else {
        error.removeAttribute("hidden");
        error.innerHTML = "请先输入手机号码";
    }
}

function time(btn) {
    if (wait == 1) {
        btn.removeAttribute("disabled");
        btn.innerHTML = "重新获取验证码";
        wait = 60;
    } else {
        var input = document.getElementById("with_code_input");
        input.style.display = "inline-block";
        input.style.width = "415px";
        btn.setAttribute("disabled", true);
        btn.innerHTML = wait + "秒后重新发送";
        wait--;
        setTimeout(function () {
            time(btn)
        }, 1000)
        }
}

function send_msg_with_phone() {
    var input = check_input();
    var btn = document.getElementById("send_msg");
    if (input) {
        var base_url = document.location.toString();
        $.post('/send_msg/', {"phone_number": input, "base_url": base_url}, time(btn));
    }
}

function send_msg_without_phone(){
    var base_url = document.location.toString();
    var btn = document.getElementById("send_msg");
    $.post('/send_msg/', {"base_url": base_url}, time(btn));

}

function time_p() {

}



function send_code_when_register() {
    var input = check_input();
    var base_url = document.location.toString();
    var p_text = document.getElementById();
    if (input) {
        $.post('/send_msg/', {"base_url": base_url}, time_p(p));
    }
}


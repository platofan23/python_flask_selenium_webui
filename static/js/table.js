//Global variables 
var t_name_clicked = false;
var t_des_clicked = false;
//Let HTML document finish loading
$(window).bind('load', function() {
    //Get the Table via JQuery
    const $tableID = $('#table');
    if ($tableID === 'undefined' || typeof($tableID) == 'undefined') {
        alert(String('Table does not exist!'));
    } else {
        //Refresh Table every 15 Seconds
        setInterval(function() {
            $('.table').load(location.href + ' .table');
        }, 30000);

        $('.table-add').on('click', 'i', () => {
            //Appending a form to a model window
            $('<div class="formContainer"></div>').appendTo('.modal-content');
            $('<form onsubmit="sendData()" id="form1" action="javascript:;" method="post" enctype="multipart/form-data" accept-charset="utf-8" class="decor" novalidate></form>').appendTo('.formContainer')
            $('<div class="form-left-decoration"></div>').appendTo('#form1');
            $('<div class="form-right-decoration"></div>').appendTo('#form1');
            $('<div class="circle"></div>').appendTo('#form1');
            $('<div class="form-inner"></div>').appendTo('#form1');
            $('<h1> Add new Test </h1>').appendTo('.form-inner');
            $('<input type="text" placeholder="Testname" name="t_name" maxlength="20" autocomplete="off" pattern=".*.py" autofocus required formmethod="post"  formenctype="multipart/form-data">').appendTo('.form-inner');
            $('<input type="email " placeholder="Description " name="t_des" maxlength="50 " autocomplete="off " required formmethod="post"  formenctype="multipart/form-data">').appendTo('.form-inner');
            $('<textarea placeholder="Seleniumcode here " id="t_sel" name="t_sel " autocomplete="off " required></textarea>').appendTo('.form-inner');
            $('<button type="submit " formmethod="post"  formenctype="multipart/form-data" > Submit</button>').appendTo('.form-inner');
            //Showing the window
            $('#myModal').show();
        });

        //Modal window for showing the log of a test
        $tableID.on('click', '.teststate', function() {
            let number = Number(parseInt($(this).parent().parent().find('td:eq(0)').text()));
            //Check the Number
            if (testNumber(number) !== 'okay') {
                alert(String(testNumber(number)));
            } else {
                //Check if number exists
                if (numberExist(number) !== 'okay') {
                    alert(String('Number does not exist!'));
                } else {
                    //Ajax-Call to get the Log
                    $.ajax({
                        data: {
                            number: number,
                        },
                        type: 'POST',
                        url: '/T_List',
                        success: function(response) {
                            //Appending the list to a modal window
                            $('<div class="formcontainer2"></div>').appendTo('.modal-content');
                            $('<div class="container"></div').appendTo('.formcontainer2');
                            $('<div class="items"></div').appendTo('.container');
                            $('<div class="items-head"></div').appendTo('.items');
                            $('<p>Log</p>').appendTo('.items-head');
                            $('<hr>').appendTo('.items-head');
                            $('<div class="items-body"></div>').appendTo('.items');
                            $('<div class="items-body-content"></div>').appendTo('.items-body');
                            for (var i of response.list_log) {
                                //Case log created
                                if (i.endsWith('Created')) {
                                    $('<span class="Created">' + i + '</span>').appendTo('.items-body-content');
                                    $('<br>').appendTo('.items-body-content');
                                }
                                //Case log success
                                if (i.endsWith('Success')) {
                                    $('<span class="Success">' + i + '</span>').appendTo('.items-body-content');
                                    $('<br>').appendTo('.items-body-content');
                                }
                                //Case log failed
                                if (i.endsWith('Failed')) {
                                    $('<span class="Failed">' + i + '</span>').appendTo('.items-body-content');
                                    $('<br>').appendTo('.items-body-content');
                                }
                            }
                            //Show the modal window
                            $('#myModal').show();
                            //Reload the table
                            setTimeout(function() {
                                $('.table').load(location.href + ' .table');
                            }, 500);
                        },
                        error: function(xhr) {
                            alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                        }
                    });
                }
            }
        });

        //Clicking the edit-Symbol
        $tableID.on('click', '.table-edit', function() {
            let name = String($(this).parent().parent().find('td:eq(1)').text()).trim();
            let description = String($(this).parent().parent().find('td:eq(2)').text()).trim();
            let number = Number(parseInt($(this).parent().parent().find('td:eq(0)').text()));
            let patt = /(([A-Z]|[a-z]|[0-9])*.py$)/i;
            //Check number
            if (testNumber(number) !== 'okay') {
                alert(String(testNumber(number)));
            } else {
                //Check name
                if (testString(name) !== 'okay') {
                    alert(String(testString(name)));
                } else {
                    //Check discription
                    if (testString(description) !== 'okay') {
                        alert(String(testString(description)));
                    } else {
                        //Check the name via pattern
                        if (patt.test(name) === false || name.endsWith('.py') === false) {
                            alert(String('Name not matisching with .py'));
                        } else {
                            //Check if number exists
                            if (numberExist(number) !== 'okay') {
                                alert(String('Number does not exist!'));
                            } else {
                                //Only do if name was changed
                                if (t_name_clicked === true) {
                                    //Look if name already exists
                                    if (nameExist(name) === 'nope') {
                                        //Ajax-Call to change the name
                                        $.ajax({
                                            data: {
                                                name: name,
                                                number: number
                                            },
                                            type: 'POST',
                                            url: '/T_ChangeName',
                                            success: function(response) {
                                                //Check if change was successful
                                                if (response.state != 'okay') {
                                                    alert(String(response.state));
                                                }
                                                //Reload the table
                                                setTimeout(function() {
                                                    $('.table').load(location.href + ' .table');
                                                }, 500);
                                            },
                                            error: function(xhr) {
                                                alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                                            }
                                        });
                                    } else {
                                        alert('Name is already used!');
                                    }
                                }
                                //Only do if description was changed
                                if (t_des_clicked === true) {
                                    //Ajax-Call to change description
                                    $.ajax({
                                        data: {
                                            description: description,
                                            number: number,
                                        },
                                        type: 'POST',
                                        url: '/T_ChangeDes',
                                        success: function(response) {
                                            //Check if change was successful
                                            if (response.state != 'okay') {
                                                alert(String(response.state));
                                            }
                                            //Reload the table
                                            setTimeout(function() {
                                                $('.table').load(location.href + ' .table');
                                            }, 500);
                                        },
                                        error: function(xhr) {
                                            alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                                        }
                                    });
                                }
                            }
                        }
                    }
                }
            }
            //Reset the clicked-check-variable
            t_name_clicked = false;
            t_des_clicked = false;
        });

        //Clicking on the name
        $tableID.on('click', '.t_name', function() {
            t_name_clicked = true;
        });

        //Clicking on the description
        $tableID.on('click', '.t_des', function() {
            t_des_clicked = true;
        });

        //Clicking the remove-Symbol
        $tableID.on('click', '.table-remove', function() {
            let name = String($(this).parent().parent().find('td:eq(1)').text()).trim();
            let number = Number(parseInt($(this).parent().parent().find('td:eq(0)').text()));
            //Check number
            if (testNumber(number) !== 'okay') {
                alert(String(testNumber(number)));
            } else {
                //Check name
                if (testString(name) !== 'okay') {
                    alert(String(testString(name)));
                } else {
                    //Check if name exists
                    if (nameExist(name) !== 'okay') {
                        alert(String('Name does not exist!'));
                    } else {
                        //Check if number exists
                        if (numberExist(number) !== 'okay') {
                            alert(String("Number does not exist!"));
                        } else {
                            //Ajax-Call to delete a test
                            $.ajax({
                                data: {
                                    name: name,
                                    number: number
                                },
                                type: 'POST',
                                url: '/T_Del',
                                success: function(response) {
                                    //Check if delete was successful
                                    if (String(response.state) !== 'okay') {
                                        alert(String(response.state));
                                    }
                                    //Reload the table
                                    setTimeout(function() {
                                        $('.table').load(location.href + ' .table');
                                    }, 500);
                                },
                                error: function(xhr) {
                                    alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                                }
                            });
                        }
                    }
                }
            }
        });

        //Clicking the run-Symbol
        $tableID.on('click', '.table-run', function() {
            let name = String($(this).parent().parent().find('td:eq(1)').text()).trim();
            let number = Number(parseInt($(this).parent().parent().find('td:eq(0)').text()));
            //Check number
            if (testNumber(number) !== 'okay') {
                alert(testNumber(String(number)));
            } else {
                //Check name
                if (testString(name) !== 'okay') {
                    alert(String(testString(name)));
                } else {
                    //Check if name exists
                    if (nameExist(name) !== 'okay') {
                        alert(String('Name does not exist!'));
                    } else {
                        //Check if number exists
                        if (numberExist(number) !== 'okay') {
                            alert(String("Number does not exist!"));
                        } else {
                            //Ajax-Call to run a test
                            $.ajax({
                                data: {
                                    name: name,
                                    number: number
                                },
                                type: 'POST',
                                url: '/T_Run',
                                success: function(response) {
                                    //Check if the run was successful
                                    if (String(response.state) != 'okay') {
                                        alert(String(response.state));
                                    }
                                    //Reload the table
                                    setTimeout(function() {
                                        $('.table').load(location.href + ' .table');
                                    }, 500);
                                },
                                error: function(xhr) {
                                    alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                                }
                            });
                        }
                    }
                }
            }
        });

        //Clicking the Code-Symbol
        $tableID.on('click', '.code-edit', function() {
            let name = String($(this).parent().parent().find('td:eq(1)').text()).trim();
            //Check name
            if (testString(name) != 'okay') {
                alert(String(testString(name)));
            } else {
                //Check if name exists
                if (String(nameExist(name)) !== 'okay') {
                    alert(String('Name does not exist!'));
                } else {
                    //Ajax-Call to get the code
                    $.ajax({
                        data: {
                            name: name,
                        },
                        type: 'POST',
                        url: '/T_Code',
                        success: function(response) {
                            //Check the call was successfull
                            if (response.state === 'okay') {
                                //Building the textarea in a model-window
                                $('<div class="formcontainer2"></div>').appendTo('.modal-content');
                                $('<textarea id="txt" rows="22" style="width:100%; height:100%;" placeholder="Seleniumcode here" name="t_sel" autocomplete="off" required></textarea>').appendTo('.formcontainer2');
                                $('<button id="button" type="button" onclick="javascript:changeCode()">Submit</button>').appendTo('.formcontainer2');
                                $("#txt").text(response.code)
                                $("#txt").attr('class', name)
                                    //Show the modal-window
                                $('#myModal').show();
                            } else {
                                alert(String('Data does not exist!'));
                            }
                        },
                        error: function(xhr) {
                            alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                        }
                    });
                }
            }
        });

        //Hiding Modal-Window for the log
        $('.close').on('click', function() {
            //Check 
            if ($('#loglist') !== 'undefined' || typeof($('#loglist')) !== 'undefined') {
                //Remove
                $('#loglist').remove();
            }
            //Check
            if ($('.formcontainer') !== 'undefined' || typeof($('.formcontainer')) !== 'undefined') {
                //Remove
                $('.formcontainer').remove();
            }
            //Check
            if ($('.formcontainer2') !== 'undefined' || typeof($('.formcontainer2')) !== 'undefined') {
                //Remove
                $('.formcontainer2').remove();
            }
            //Check
            if ($('#txt') !== 'undefined' || typeof($('#text')) != 'undefined') {
                //Remove
                $('#txt').remove();
            }
            //Check
            if ($('#myModal') !== 'undefined' || typeof($('#myModal')) != 'undefined') {
                //Hide
                $('#myModal').hide();
            }
        });
    }
});

//Clicking the submit-Button of the form
function sendData() {
    let name = String($('input[name = t_name]').val()).trim();
    let description = String($('input[name = t_des]').val()).trim();
    let code = $('#t_sel').val().trim();
    let patt = /(([A-Z]|[a-z]|[0-9])*.py$)/i;
    //Check name
    if (testString(name) !== 'okay') {
        alert(String(testString(name)));
    } else {
        //Check description
        if (testString(description) != 'okay') {
            alert(String(testString(description)));
        } else {
            //Check code
            if (testString(code) != 'okay') {
                alert(String(testString(code)));
            } else {
                //Check name via pattern
                if (patt.test(name) == false || name.endsWith(".py") == false) {
                    alert(String("Name matscht nicht mit .py"));
                } else {
                    //Check if name already exists
                    if (nameExist(name) !== 'nope') {
                        alert(String('Name already exists!'))
                    } else {
                        //Ajax-Call create new test
                        $.ajax({
                            data: {
                                name: name,
                                description: description,
                                code: code
                            },
                            type: 'POST',
                            url: '/T_New',
                            success: function(response) {
                                //Check if the create was successfull
                                if (String(response.state) != 'okay') {
                                    alert(String(response.state));
                                }
                                if ($('.formcontainer') === 'undefined' || typeof($('.formcontainer')) == 'undefined' || $('#myModal') === 'undefined' || typeof($('#myModal')) == 'undefined') {
                                    alert(String('Form does not exist!'))
                                } else {
                                    //Hide the form
                                    $('#myModal').hide();
                                    $('.formContainer').hide();
                                    $('.formContainer').remove();
                                }
                                //Reload the table
                                setTimeout(function() {
                                    $('.table').load(location.href + ' .table');
                                }, 500);
                            },
                            error: function(xhr) {
                                alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                            }
                        });
                    }
                }
            }
        }
    }
}

//Clicking the submit-Button of the form
function changeCode() {
    let name = String($('#txt').attr('class')).trim();
    let code = String($('#txt').val());
    //Check name
    if (testString(name) != 'okay') {
        alert(String(testString(name)));
    } else {
        //Check code
        if (testString(code) != 'okay') {
            alert(String(testString(code)));
        } else {
            //Check if name exists
            if (nameExist(name) === 'nope') {
                alert(String('Name does not exist!'));
            } else {
                //Ajax-Call changing the code
                $.ajax({
                    data: {
                        name: name,
                        code: code
                    },
                    type: 'POST',
                    url: '/T_ChangeCode',
                    success: function(response) {
                        //Check if the change was successful
                        if (String(response.state) != 'okay') {
                            alert(String(response.state));
                        }
                        if ($('.formcontainer2') === 'undefined' || typeof($('.formcontainer2')) == 'undefined' || $('#myModal') === 'undefined' || typeof($('#myModal')) == 'undefined') {
                            alert(String('Form does not exist!'))
                        } else {
                            //Hide the form
                            $('#myModal').hide();
                            $('.formContainer2').hide();
                            $('.formContainer2').remove();
                        }
                        setTimeout(function() {
                            $('.table').load(location.href + ' .table');
                        }, 500);
                    },
                    error: function(xhr) {
                        alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                    }
                });
            }
        };
    }
}

//Function Number exists
function numberExist(number) {
    number = Number(number);
    let back = String('');
    //Ajax-Call number exist
    $.ajax({
        data: {
            number: number,
        },
        type: 'POST',
        url: '/T_Num',
        async: false,
        success: function(response) {
            //See what the response of the call is
            if (response.state === 'nope') {
                back = String('nope');
            } else {
                back = String('okay');
            }
        },
        error: function(xhr) {
            return String('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText).trim();
        }
    });
    return String(back);
}

//Function Name exists
function nameExist(name) {
    name = String(name);
    let back = String('');
    //Ajax-Call name exist
    $.ajax({
        data: {
            name: name,
        },
        type: 'POST',
        url: '/T_Name',
        async: false,
        success: function(response) {
            //See what the response of the call is
            if (response.state === 'nope') {
                back = String('nope')
            } else {
                back = String('okay');
            }
        },
        error: function(xhr) {
            return String('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText).trim();
        }
    });
    return String(back);
}

//Function to validate a number
function testNumber(num) {
    num = Number(num);
    let back = String('');
    //Check undefined
    if (num === 'undefined' || typeof(num) == 'undefined') {
        back = String('Number is undefined!');
    } else {
        //Check NaN
        if (Number.isNaN(num)) {
            back = String('Number is NaN!');
        } else {
            //Check number finite
            if (Number.isFinite(num) === false) {
                back = String('Number is not finite!');
            } else {
                //Check whole number
                if (Number.isInteger(num) === false && Number.isSafeInteger(num) === false) {
                    back = String('Number is not an Integer!');
                } else {
                    //Check in area
                    if (num < 0 || num === Infinity || num === -Infinity) {
                        back = String('Number out of the area!');
                    } else {
                        back = String('okay');
                    }
                }
            }
        }
    }
    return String(back);
}

function testString(str) {
    str = String(str);
    let back = String('');
    //Check undefined
    if (str === 'undefined' || typeof(str) == 'undefined') {
        back = String('String is undefined!');
    } else {
        //Check string empty
        if (str.length === 0 || str === '' || str === ' ') {
            back = String('String is empty!');
        } else {
            back = String('okay');
        }
    }
    return String(back);
}
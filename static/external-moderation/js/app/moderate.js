/* global requirejs */

requirejs.config({
  shim: {
    jquery: {
      exports: '$'
    },
    cookie: {
      exports: 'Cookies'
    },
  },
  baseUrl: '/static/external-approvals/js/app',
  paths: {
    app: '/static/builder-js/js/app',
    material: '/static/builder-js/vendor/material-components-web-11.0.0',
    jquery: '/static/builder-js/vendor/jquery-3.4.0.min',
    cookie: '/static/builder-js/vendor/js.cookie'
  }
})

requirejs(['material', 'cookie', 'jquery'], function (mdc, Cookies) {
  const csrftoken = $('[name=csrfmiddlewaretoken]').val()

  function csrfSafeMethod (method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
  }

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', csrftoken)
      }
    }
  })

  const responseElement = document.getElementById('response-field')
    
  if (responseElement !== null) {
	  const topAppBar = mdc.topAppBar.MDCTopAppBar.attachTo(document.getElementById('app-bar'))
	
	  topAppBar.setScrollTarget(document.getElementById('main-content'))
	  
	  const responseField = mdc.textField.MDCTextField.attachTo(responseElement)
	  
	  $('.action-button').click(function(eventObj) {
		const payload = {
			action: 'deny',
			response: responseField.value
		}
		
		if (eventObj.currentTarget.id === 'action-approve') {
			payload['action'] = 'approve'
		}
		
		$.post('moderate', payload, function(data, textStatus, jqXHR) {
			if (data.success) {
				window.alert('Approval moderated.')
				
				window.location.reload()
			}
		})
	  })
	}
})

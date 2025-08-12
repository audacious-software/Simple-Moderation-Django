define(['material', 'cards/node', 'jquery'], function (mdc, Node) {
  class ExternalModerationNode extends Node {
    editBody () {
      const destinationNodes = this.destinationNodes(this)

      let body = '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-12">'
      body += '  <label class="mdc-text-field mdc-text-field--outlined mdc-text-field--textarea" id="' + this.cardId + '_message" style="width: 100%">'
      body += '    <span class="mdc-notched-outline">'
      body += '      <span class="mdc-notched-outline__leading"></span>'
      body += '      <div class="mdc-notched-outline__notch">'
      body += '        <label for="' + this.cardId + '_message_value" class="mdc-floating-label">Message</label>'
      body += '      </div>'
      body += '      <span class="mdc-notched-outline__trailing"></span>'
      body += '    </span>'
      body += '    <span class="mdc-text-field__resizer">'
      body += '      <textarea class="mdc-text-field__input" rows="4" style="width: 100%" id="' + this.cardId + '_message_value"></textarea>'
      body += '    </span>'
      body += '  </label>'
      body += '</div>'

      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-12">'
      body += '  <div class="mdc-text-field mdc-text-field--outlined" id="' + this.cardId + '_response" style="width: 100%">'
      body += '    <input class="mdc-text-field__input" type="text" id="' + this.cardId + '_response_value">'
      body += '    <div class="mdc-notched-outline">'
      body += '      <div class="mdc-notched-outline__leading"></div>'
      body += '      <div class="mdc-notched-outline__notch">'
      body += '        <label for="' + this.cardId + '_response_value" class="mdc-floating-label">Response Variable Name</label>'
      body += '      </div>'
      body += '      <div class="mdc-notched-outline__trailing"></div>'
      body += '    </div>'
      body += '  </div>'
      body += '</div>'

      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-8">'
      body += '  <div class="mdc-typography--subtitle2">Approved:</div>'
      body += '</div>'
      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-4" style="text-align: right;">'
      body += '  <button class="mdc-icon-button" id="' + this.cardId + '_approve_edit">'
      body += '    <i class="material-icons mdc-icon-button__icon" aria-hidden="true">create</i>'
      body += '  </button>'

      let found = false

      for (let j = 0; j < destinationNodes.length; j++) {
        const destinationNode = destinationNodes[j]

        if (this.definition.approve_action !== undefined) {
          if (destinationNode.id === this.definition.approve_action) {
            found = true
          }
        }
      }

      if (found === false && this.definition.approve_action !== undefined) {
        const node = this.dialog.resolveNode(this.definition.approve_action)

        if (node !== null) {
          found = true
        }
      }

      if (found) {
        body += '  <button class="mdc-icon-button" id="' + this.cardId + '_approve_click">'
        body += '    <i class="material-icons mdc-icon-button__icon" aria-hidden="true">navigate_next</i>'
        body += '  </button>'
      }

      body += '</div>'

      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-8">'
      body += '  <div class="mdc-typography--subtitle2">Denied:</div>'
      body += '</div>'
      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-4" style="text-align: right;">'
      body += '  <button class="mdc-icon-button" id="' + this.cardId + '_deny_edit">'
      body += '    <i class="material-icons mdc-icon-button__icon" aria-hidden="true">create</i>'
      body += '  </button>'

      found = false

      for (let j = 0; j < destinationNodes.length; j++) {
        const destinationNode = destinationNodes[j]

        if (this.definition.deny_action !== undefined) {
          if (destinationNode.id === this.definition.deny_action) {
            found = true
          }
        }
      }

      if (found === false && this.definition.deny_action !== undefined) {
        const node = this.dialog.resolveNode(this.definition.deny_action)

        if (node !== null) {
          found = true
        }
      }

      if (found) {
        body += '  <button class="mdc-icon-button" id="' + this.cardId + '_deny_click">'
        body += '    <i class="material-icons mdc-icon-button__icon" aria-hidden="true">navigate_next</i>'
        body += '  </button>'
      }

      body += '</div>'

      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-4">'
      body += '  <div class="mdc-typography--subtitle2">Timeout:</div>'
      body += '</div>'
      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-4">'
      body += '  <div class="mdc-text-field mdc-text-field--outlined" id="' + this.cardId + '_timeout_seconds"  style="width: 100%">'
      body += '    <input type="number" min="0" step="1" class="mdc-text-field__input" id="' + this.cardId + '_timeout_seconds_value">'
      body += '    <div class="mdc-notched-outline">'
      body += '      <div class="mdc-notched-outline__leading"></div>'
      body += '      <div class="mdc-notched-outline__notch">'
      body += '        <label for="' + this.cardId + '_timeout_seconds_value" class="mdc-floating-label">Seconds</label>'
      body += '      </div>'
      body += '      <div class="mdc-notched-outline__trailing"></div>'
      body += '    </div>'
      body += '  </div>'
      body += '  <a class="mdc-typography--caption" href="#" id="' + this.cardId + '_clear_timeout" style="display: inline-block; padding-left: 4px;">Clear Timeout</a>'
      body += '</div>'

      body += '<div class="mdc-layout-grid__cell mdc-layout-grid__cell--span-4" style="text-align: right;">'

      body += '  <button class="mdc-icon-button" id="' + this.cardId + '_timeout_edit">'
      body += '    <i class="material-icons mdc-icon-button__icon" aria-hidden="true">create</i>'
      body += '  </button>'

      found = false

      for (let j = 0; j < destinationNodes.length; j++) {
        const destinationNode = destinationNodes[j]

        if (this.definition.timeout_action !== undefined) {
          if (destinationNode.id === this.definition.timeout_action) {
            found = true
          }
        }
      }

      if (found === false && this.definition.timeout_action !== undefined) {
        const node = this.dialog.resolveNode(this.definition.timeout_action)

        if (node !== null) {
          found = true
        }
      }

      if (found) {
        body += '  <button class="mdc-icon-button" id="' + this.cardId + '_timeout_click">'
        body += '    <i class="material-icons mdc-icon-button__icon" aria-hidden="true">navigate_next</i>'
        body += '  </button>'
      }

      body += '</div>'

      body += '<div class="mdc-dialog" role="alertdialog" aria-modal="true" id="' + this.cardId + '-edit-dialog"  aria-labelledby="' + this.cardId + '-dialog-title" aria-describedby="' + this.cardId + '-dialog-content">'
      body += '  <div class="mdc-dialog__container">'
      body += '    <div class="mdc-dialog__surface">'
      body += '      <h2 class="mdc-dialog__title" id="' + this.cardId + '-dialog-title">Choose Destination</h2>'
      body += '      <div class="mdc-dialog__content" id="' + this.cardId + '-dialog-content" style="padding: 0px;">'
      body += this.dialog.chooseDestinationMenu(this.cardId)
      body += '      </div>'
      //            body += '      <footer class="mdc-dialog__actions">';
      //            body += '        <button type="button" class="mdc-button mdc-dialog__button" data-mdc-dialog-action="close">';
      //            body += '          <span class="mdc-button__label">Save</span>';
      //            body += '        </button>';
      //            body += '      </footer>';
      body += '    </div>'
      body += '  </div>'
      body += '  <div class="mdc-dialog__scrim"></div>'
      body += '</div>'

      return body
    }

    viewBody () {
      let summary = '<div class="mdc-typography--body1" style="margin-top: 16px; margin-left: 16px; margin-right: 16px; margin-bottom: 8px;">Continue after moderating...</div>'

      summary += `<div class="mdc-typography--body1" style="margin-left: 16px; margin-right: 16px; margin-bottom: 16px;"><em>${this.definition.message}</em></div>`

      const approveNode = this.dialog.resolveNode(this.definition.approve_action)

      if (approveNode !== null) {
        summary += `<div class="mdc-typography--body1" style="margin-left: 16px; margin-right: 16px; margin-bottom: 16px;">If approved, go to: ${approveNode.cardName()}.</div>`
      }

      const denyNode = this.dialog.resolveNode(this.definition.deny_action)

      if (denyNode !== null) {
        summary += `<div class="mdc-typography--body1" style="margin-left: 16px; margin-right: 16px; margin-bottom: 16px;">If denied, go to: ${denyNode.cardName()}.</div>`
      }

      if (this.definition.timeout_action !== undefined) {
        const timeoutNode = this.dialog.resolveNode(this.definition.timeout_action)

        if (timeoutNode !== null) {
          summary += `<div class="mdc-typography--body1" style="margin-left: 16px; margin-right: 16px; margin-bottom: 16px;">If timed out: ${timeoutNode.cardName()}.</div>`
        }
      }

      return summary
    }

    initialize () {
      super.initialize()

      const me = this

      const nextDialog = mdc.dialog.MDCDialog.attachTo(document.getElementById(me.cardId + '-edit-dialog'))

      const messageField = mdc.textField.MDCTextField.attachTo(document.getElementById(this.cardId + '_message'))

      if (this.definition.message !== undefined) {
        messageField.value = this.definition.message
      }

      $('#' + this.cardId + '_message_value').on('change keyup paste', function () {
        const value = $('#' + me.cardId + '_message_value').val()

        me.definition.message = value

        me.dialog.markChanged(me.id)
      })

      const responseVariableField = mdc.textField.MDCTextField.attachTo(document.getElementById(this.cardId + '_response'))

      if (this.definition.response_variable !== undefined) {
        responseVariableField.value = this.definition.response_variable
      }

      $('#' + this.cardId + '_response_value').on('change keyup paste', function () {
        const value = $('#' + me.cardId + '_response_value').val()

        me.definition.response_variable = value

        me.dialog.markChanged(me.id)
      })

      $('#' + this.cardId + '_clear_timeout').on('click', function (eventObj) {
        eventObj.preventDefault()

        if (window.confirm('Reset timeout options?')) {
          delete me.definition.timeout_interval
          delete me.definition.timeout_action

          me.dialog.loadNode(me.definition)

          me.dialog.markChanged(me.id)
        }
      })

      this.dialog.initializeDestinationMenu(me.cardId, function (selected) {
        if (me.targetAction === 'timeout') {
          me.definition.timeout_action = selected
        } else if (me.targetAction === 'approve') {
          me.definition.approve_action = selected
        } else {
          me.definition.deny_action = selected
        }

        me.dialog.markChanged(me.id)
        me.dialog.loadNode(me.definition)
      })

      $('#' + this.cardId + '_approve_edit').on('click', function () {
        me.targetAction = 'approve'

        nextDialog.open()
      })

      $('#' + this.cardId + '_deny_edit').on('click', function () {
        me.targetAction = 'deny'

        nextDialog.open()
      })

      $('#' + this.cardId + '_timeout_edit').on('click', function () {
        me.targetAction = 'timeout'

        nextDialog.open()
      })

      $('#' + this.cardId + '_approve_click').on('click', function () {
        const destinationNodes = me.destinationNodes(me.dialog)

        for (let i = 0; i < destinationNodes.length; i++) {
          const destinationNode = destinationNodes[i]

          if (me.definition.approve_action === destinationNode.id) {
            $("#builder_next_nodes [data-node-id='" + destinationNode.id + "']").css('background-color', '#ffffff')
          } else {
            $("#builder_next_nodes [data-node-id='" + destinationNode.id + "']").css('background-color', '#e0e0e0')
          }
        }

        const sourceNodes = me.sourceNodes(me.dialog)

        for (let i = 0; i < sourceNodes.length; i++) {
          const sourceNode = sourceNodes[i]

          if (me.definition.approve_action === sourceNode.id) {
            $("#builder_source_nodes [data-node-id='" + sourceNode.id + "']").css('background-color', '#ffffff')
          } else {
            $("#builder_source_nodes [data-node-id='" + sourceNode.id + "']").css('background-color', '#e0e0e0')
          }
        }
      })

      $('#' + this.cardId + '_deny_click').on('click', function () {
        const destinationNodes = me.destinationNodes(me.dialog)

        for (let i = 0; i < destinationNodes.length; i++) {
          const destinationNode = destinationNodes[i]

          if (me.definition.deny_action === destinationNode.id) {
            $("#builder_next_nodes [data-node-id='" + destinationNode.id + "']").css('background-color', '#ffffff')
          } else {
            $("#builder_next_nodes [data-node-id='" + destinationNode.id + "']").css('background-color', '#e0e0e0')
          }
        }

        const sourceNodes = me.sourceNodes(me.dialog)

        for (let i = 0; i < sourceNodes.length; i++) {
          const sourceNode = sourceNodes[i]

          if (me.definition.deny_action === sourceNode.id) {
            $("#builder_source_nodes [data-node-id='" + sourceNode.id + "']").css('background-color', '#ffffff')
          } else {
            $("#builder_source_nodes [data-node-id='" + sourceNode.id + "']").css('background-color', '#e0e0e0')
          }
        }
      })

      $('#' + this.cardId + '_timeout_click').on('click', function () {
        const destinationNodes = me.destinationNodes(me.dialog)

        for (let i = 0; i < destinationNodes.length; i++) {
          const destinationNode = destinationNodes[i]

          if (me.definition.timeout_action === destinationNode.id) {
            $("#builder_next_nodes [data-node-id='" + destinationNode.id + "']").css('background-color', '#ffffff')
          } else {
            $("#builder_next_nodes [data-node-id='" + destinationNode.id + "']").css('background-color', '#e0e0e0')
          }
        }

        const sourceNodes = me.sourceNodes(me.dialog)

        for (let i = 0; i < sourceNodes.length; i++) {
          const sourceNode = sourceNodes[i]

          if (me.definition.timeout_action === sourceNode.id) {
            $("#builder_source_nodes [data-node-id='" + sourceNode.id + "']").css('background-color', '#ffffff')
          } else {
            $("#builder_source_nodes [data-node-id='" + sourceNode.id + "']").css('background-color', '#e0e0e0')
          }
        }
      })

      const timeoutSecondsField = mdc.textField.MDCTextField.attachTo(document.getElementById(this.cardId + '_timeout_seconds'))

      if (this.definition.timeout_interval !== undefined) {
        timeoutSecondsField.value = this.definition.timeout_interval
      }

      $('#' + this.cardId + '_timeout_seconds_value').change(function (eventObj) {
        const value = $('#' + me.cardId + '_timeout_seconds_value').val()

        if (value === '') {
          delete me.definition.timeout_interval
          delete me.definition.timeout_action
        } else {
          me.definition.timeout_interval = parseInt(value)
        }

        me.dialog.markChanged(me.id)
      })
    }

    destinationNodes (dialog) {
      const nodes = super.destinationNodes(dialog)

      const destinations = [
        this.definition.approve_action,
        this.definition.deny_action,
        this.definition.timeout_action
      ]

      const includedIds = []

      for (let j = 0; j < destinations.length; j++) {
        const id = destinations[j]

        if (id !== undefined && id !== null) {
          for (let i = 0; i < dialog.definition.length; i++) {
            const item = dialog.definition[i]

            if (item.id === id) {
              nodes.push(Node.createCard(item, dialog))
            }
          }

          includedIds.push(id)
        }
      }

      return nodes
    }

    updateReferences (oldId, newId) {
      $.each(this.actions, function (index, value) {
        if (value.action === oldId) {
          value.action = newId
        }
      })
    }

    cardType () {
      return 'External Moderation'
    }

    static cardName () {
      return 'External Moderation'
    }

    static createCard (cardName) {
      const id = Node.uuidv4()

      const card = {
        type: 'external-moderation',
        name: cardName,
        id,
        approve_action: null,
        deny_action: null,
        timeout_action: null,
        timeout_interval: (24 * 3600),
        message: '(Enter message to pass to moderators here...)'
      }

      return card
    }
  }

  Node.registerCard('external-moderation', ExternalModerationNode)

  return ExternalModerationNode
})

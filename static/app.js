class Chatbox {
  constructor() {
    this.args = {
      openBtn: document.querySelector(".icon-chatbot-button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendBtn: document.querySelector(".send__button"),
    };

    this.state = false;
    this.messages = [];
  }

  display() {
    const { openBtn, chatBox, sendBtn } = this.args;

    openBtn.addEventListener("click", () => this.toggleState(chatBox));

    sendBtn.addEventListener("click", () => this.onSendBtn(chatBox));

    const node = chatBox.querySelector(".ques-input");
    node.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendBtn(chatBox);
      }
    });
  }

  toggleState(chatbox) {
    this.state = !this.state;
    if (this.state) {
      chatbox.classList.add("chatbox--active");
    } else {
      chatbox.classList.remove("chatbox--active");
    }
  }

  onSendBtn(chatbox) {
    var textField = chatbox.querySelector(".ques-input");
    let text1 = textField.value;
    if (text1 === "") {
      return;
    }

    let msg1 = { name: "User", message: text1 };
    this.messages.push(msg1);

    fetch($SCRIPT_ROOT + "/predict", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      node: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        let msg2 = { name: "BOT", message: r.answer, tag: r.tag };
        this.messages.push(msg2);
        this.updateChatText(chatbox);
        textField.value = "";
      })
      .catch((error) => {
        console.error("Error: ", error);
        this.updateChatText(chatbox);
        textField.value = "";
      });
  }

  updateChatText(chatbox) {
    var html = "";
    this.messages
      .slice()
      .reverse()
      .forEach(function (item) {
        if (item.name === "BOT") {
          if (item.tag !== "none") {
            html +=
              '<div class="linkcourse messages__item messages__item--visitor">' +
              '<a target="_blank" href="http://127.0.0.1:8080/product/' +
              item.tag +
              '" >' +
              "Khóa học " +
              item.tag +
              "</a>" +
              "</div>";
            html +=
              '<div class="messages__item messages__item--visitor">' +
              item.message +
              "</div>";
          } else {
            html +=
              '<div class="messages__item messages__item--visitor">' +
              item.message +
              "</div>";
          }
        } else {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.message +
            "</div>";
        }
      });
    const chatmessage = chatbox.querySelector("#chatbox__messages");
    chatmessage.innerHTML = html;
  }
}

const chatbox = new Chatbox();
chatbox.display();

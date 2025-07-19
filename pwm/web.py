import os
import webbrowser
import tempfile
from dataclasses import  asdict
from rich.console import Console
from pwm.storage import  Storage
from pwm import errors


CSS = """body {
  background-color: rgb(28, 21, 48);
  font-family: "Kanit", sans-serif;
  padding: 0;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.title {
  display: flex;
  align-items: center;
  padding: 5rem 0 0 0;
}

.title__line {
  flex-grow: 1;
  height: 0.2rem;
  background: #5ab0f7;
}

.title__text {
  font-size: 3.6rem;
  color: #5ab0f7;
  white-space: nowrap;
  padding: 0 1rem;
  font-weight: 600;
}

.app {
  border: 0.2rem solid #5ab0f7;
  border-radius: 1rem;
  color: #5ab0f7;
  /* max-width: 40vw; */
  margin: 8rem 20vw;
  max-height: 40vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.app__name {
  text-align: center;
  font-size: 1.8rem;
  border-bottom: 0.2rem solid #5ab0f7;
  padding: 0.2rem 0;
}

.app__passwords {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.app__password {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2.4rem;
}

.icon {
  background: none;
  border: none;
  color: rgb(228, 38, 107);
  font-size: 1rem;
  cursor: pointer;
}

.app__password {
  color: #5ab0f7;
}

.password__container {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: rgb(228, 38, 107);
}
"""

JS = """document.querySelectorAll(".copy").forEach((button) => {
  button.addEventListener("click", () => {
    const passwordSpan = button.parentElement.querySelector(
      ".password__password"
    );
    const passwordText = passwordSpan.dataset.password;

    navigator.clipboard
      .writeText(passwordText)
      .then(() => {
        const original = button.textContent;
        button.textContent = "✅";
        setTimeout(() => {
          button.textContent = original;
        }, 1000);
      })
      .catch((err) => {
        console.error("Failed to copy:", err);
      });
  });
});

document.querySelectorAll(".toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const passwordSpan = button.parentElement.querySelector(
      ".password__password"
    );

    passwordSpan.classList.toggle("visable");
    if (passwordSpan.classList.contains("visable")) {
      passwordSpan.textContent = passwordSpan.dataset.password;
    } else {
      passwordSpan.textContent = "*".repeat(
        passwordSpan.dataset.password.length
      );
    }
  });
});
"""

HTML = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Kanit:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"
      rel="stylesheet"
    />
    <style>
    {css}
    </style>
    <title>PWM Password Manager</title>
  </head>
  <body>
    <div class="title">
      <hr class="title__line" />
      <h1 class="title__text">PWM (Password Manager)</h1>
      <hr class="title__line" />
    </div>
    {apps}
    <script>{script}</script>
  </body>
</html>
"""


APP_TEMPLATE = """
    <div class="app">
      <h2 class="app__name">{app_name}</h2>
      {passwords}
    </div>

    """

PASSWORD_TEMPLATE = """
      <div class="app__passwords">
        <div class="app__password">
          <p class="password__email">Email: {email}</p>
          <div class="password__container">
            Password:
            <span
              class="password__password"
              data-password="{password}"
              >{password_stars}</span
            >
            <button class="icon toggle">👁</button>
            <button class="icon copy">📋</button>
          </div>
        </div>
      </div>

"""


def generate_web(data: dict):
    apps = []
    for app_name, passwords in data.items():
        ps = []
        for password in passwords:
            ps.append(PASSWORD_TEMPLATE.format(email=password['email'], 
                                               password=password['password'], 
                                               password_stars=f"{'*' * len(password['password'])}"))
        apps.append(APP_TEMPLATE.format(app_name=app_name.capitalize(),
                                        passwords='\n'.join(ps)))
        
    return HTML.format(
        css=CSS,
        script=JS,
        apps="\n".join(apps)
    )

def view_web(console: Console, storage: Storage, app_name: str):
    console.print(f"[] Generating web view{f' for App(name={app_name})' if app_name else ''}...", 
                justify='center', style="white bold")
    if app_name:
        try:
            data = {app_name: [asdict(d) for d in storage.view_app(app_name)]}
        except errors.DataAlreadyExists:
            console.print("[ERROR] App does not exists.", justify="center", style="bold red")
            return  
    else:
        data = storage.view_all_apps()

    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f:
        f.write(generate_web(data))
        temp_path = f.name

    webbrowser.open(f"file://{temp_path}")
    input()
    os.remove(temp_path)

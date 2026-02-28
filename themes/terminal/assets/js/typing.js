(function () {
  'use strict';

  var commands = [
    'kubectl get pods --all-namespaces',
    'go build -o server ./cmd/api',
    'terraform plan -out=deploy.tfplan',
    'docker compose up -d --build',
    'git log --oneline -10',
    'aws ecs describe-services --cluster prod',
    'helm upgrade --install api ./charts/api',
    'curl -s localhost:8080/health | jq .',
  ];

  var el = document.getElementById('typing-text');
  if (!el) return;

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    el.textContent = commands[0];
    return;
  }

  var cmdIndex = 0;
  var charIndex = 0;
  var deleting = false;
  var pauseTime = 2000;

  function type() {
    var cmd = commands[cmdIndex];

    if (!deleting) {
      charIndex++;
      el.textContent = cmd.substring(0, charIndex);

      if (charIndex === cmd.length) {
        deleting = true;
        setTimeout(type, pauseTime);
        return;
      }
      setTimeout(type, 40 + Math.random() * 60);
    } else {
      charIndex--;
      el.textContent = cmd.substring(0, charIndex);

      if (charIndex === 0) {
        deleting = false;
        cmdIndex = (cmdIndex + 1) % commands.length;
        setTimeout(type, 400);
        return;
      }
      setTimeout(type, 20 + Math.random() * 20);
    }
  }

  setTimeout(type, 800);
})();

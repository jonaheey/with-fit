const canvas = document.getElementById("canvas_hp");
const context = canvas.getContext("2d");
const width = canvas.width = 100;
const height = canvas.height = 30;

let health = 100;
var monster_status = true;

const healthBarWidth = 100;
const healthBarHeight = 30;
const x = width / 2 - healthBarWidth / 2;
const y = height / 2 - healthBarHeight / 2;

const healthBar = new HealthBar(x, y, healthBarWidth, healthBarHeight, health, "green");
const monster = new Monster();
monster.changeImageGreen();

const frame = function() {
  context.clearRect(0, 0, width, height);
  healthBar.show(context, health);
  requestAnimationFrame(frame);
}

// 운동이 카운트 될때마다 실행하는 함수로 변경해야됨
function damage(attack) {
  health -= attack;
  healthBar.updateHealth(health);

  if (health > 50 && monster_status == true){
    monster.changeImageGreen();
    monster_status = false;
  } else if (health <= 50 && health > 20 && monster_status == false){
    monster.changeImageYellow();
    monster_status = true;
  } else if (health <= 20 && health >= 0 && monster_status == true) {
    monster.changeImageRed()
    monster_status = false;
  }
};

frame();
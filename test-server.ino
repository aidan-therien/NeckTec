int data;

void setup() {
    Serial.begin(9600);
}

void loop() {
    char payload[255];
    char id[] = "1";
    float val = 98.9;
    snprintf(payload, sizeof(payload), "{\"p\":\"%s\", \"d\": %f}", id, val);
    Serial.println(payload);
    Particle.publish("post_data", payload, PRIVATE);
    delay(10000);
}
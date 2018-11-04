#include <librdkafka/rdkafka.h>

int main()
{
    printf("librdkafka version: %s\n", rd_kafka_version_str());
    return 0;
}

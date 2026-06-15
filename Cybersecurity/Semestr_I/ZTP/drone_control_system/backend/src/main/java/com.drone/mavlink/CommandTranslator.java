package com.drone.mavlink;

import com.drone.command.dto.CommandMessage;
import com.drone.mavlink.dto.MavlinkCommandPacket;

/**
 * Command translator (Epic 3.4): converts a platform {@link CommandMessage}
 * into a wire-level {@link MavlinkCommandPacket} (MAV_CMD code + params).
 */
public interface CommandTranslator {

    MavlinkCommandPacket translate(CommandMessage command);
}

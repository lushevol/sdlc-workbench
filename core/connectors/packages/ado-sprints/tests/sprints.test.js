import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureSprintsTools } from '../src/tools/sprints.js';
import { createMockServer, isValidToolResponse, isValidErrorResponse } from '@sc-node-mcp/shared-tests/helpers/mockServer';
import { createMockConnection, createMockWorkApi, createMockCoreApi, createMockWitApi } from '@sc-node-mcp/shared-tests/helpers/mockConnection';

describe('Sprint & Capacity Tools', () => {
  let mockServer;
  let mockConnection;
  let mockWorkApi;
  let mockCoreApi;
  let mockWitApi;
  let getConnectionMock;

  beforeEach(() => {
    mockServer = createMockServer();
    mockConnection = createMockConnection();
    mockWorkApi = createMockWorkApi();
    mockCoreApi = createMockCoreApi();
    mockWitApi = createMockWitApi();
    mockConnection.getWorkApi.mockResolvedValue(mockWorkApi);
    mockConnection.getCoreApi.mockResolvedValue(mockCoreApi);
    mockConnection.getWorkItemTrackingApi.mockResolvedValue(mockWitApi);
    getConnectionMock = vi.fn().mockResolvedValue(mockConnection);
    configureSprintsTools(mockServer, getConnectionMock);
  });

  describe('work_list_iterations', () => {
    it('should list all iterations for a project', async () => {
      const mockNode = { id: '1', name: 'Iterations', children: [{ id: '2', name: 'Sprint 1' }] };
      mockWitApi.getClassificationNode.mockResolvedValue(mockNode);

      const response = await mockServer.invokeTool('work_list_iterations', { project: 'TBQPR' });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.name).toBe('Iterations');
      expect(mockWitApi.getClassificationNode).toHaveBeenCalledWith('TBQPR', 1, undefined, undefined);
    });

    it('should pass depth when provided', async () => {
      mockWitApi.getClassificationNode.mockResolvedValue({ id: '1', name: 'Iterations' });
      await mockServer.invokeTool('work_list_iterations', { project: 'TBQPR', depth: 3 });
      expect(mockWitApi.getClassificationNode).toHaveBeenCalledWith('TBQPR', 1, undefined, 3);
    });

    it('should return error on API failure', async () => {
      mockWitApi.getClassificationNode.mockRejectedValue(new Error('API error'));
      const response = await mockServer.invokeTool('work_list_iterations', { project: 'TBQPR' });
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockWitApi.getClassificationNode.mockRejectedValue('raw error string');
      const response = await mockServer.invokeTool('work_list_iterations', { project: 'TBQPR' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw error string');
    });
  });

  describe('work_create_iterations', () => {
    it('should create iterations in a project', async () => {
      const created = { id: '10', name: 'Sprint 5' };
      mockWitApi.createOrUpdateClassificationNode.mockResolvedValue(created);

      const response = await mockServer.invokeTool('work_create_iterations', {
        project: 'TBQPR',
        iterations: [{ name: 'Sprint 5', startDate: '2026-05-01', finishDate: '2026-05-14' }]
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result[0].name).toBe('Sprint 5');
    });

    it('should create iteration without dates', async () => {
      mockWitApi.createOrUpdateClassificationNode.mockResolvedValue({ id: '11', name: 'Sprint 6' });
      const response = await mockServer.invokeTool('work_create_iterations', {
        project: 'TBQPR',
        iterations: [{ name: 'Sprint 6' }]
      });
      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWitApi.createOrUpdateClassificationNode).toHaveBeenCalledWith(
        expect.objectContaining({ name: 'Sprint 6' }),
        'TBQPR',
        1
      );
    });

    it('should return error on creation failure', async () => {
      mockWitApi.createOrUpdateClassificationNode.mockRejectedValue(new Error('Create error'));
      const response = await mockServer.invokeTool('work_create_iterations', {
        project: 'TBQPR',
        iterations: [{ name: 'Sprint 5' }]
      });
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockWitApi.createOrUpdateClassificationNode.mockRejectedValue('raw create error');
      const response = await mockServer.invokeTool('work_create_iterations', {
        project: 'TBQPR',
        iterations: [{ name: 'Sprint 5' }]
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw create error');
    });
  });

  describe('work_list_team_iterations', () => {
    it('should list team iterations', async () => {
      const iterations = [{ id: 'iter-1', name: 'Sprint 1' }, { id: 'iter-2', name: 'Sprint 2' }];
      mockWorkApi.getTeamIterations.mockResolvedValue(iterations);

      const response = await mockServer.invokeTool('work_list_team_iterations', {
        project: 'TBQPR',
        team: 'DCS-Abarth (SQUAD)'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });

    it('should support timeframe filter', async () => {
      mockWorkApi.getTeamIterations.mockResolvedValue([]);
      await mockServer.invokeTool('work_list_team_iterations', {
        project: 'TBQPR',
        team: 'MyTeam',
        timeframe: 'current'
      });
      expect(mockWorkApi.getTeamIterations).toHaveBeenCalledWith(
        { project: 'TBQPR', team: 'MyTeam' },
        'current'
      );
    });

    it('should return error on API failure', async () => {
      mockWorkApi.getTeamIterations.mockRejectedValue(new Error('Iteration error'));
      const response = await mockServer.invokeTool('work_list_team_iterations', {
        project: 'TBQPR',
        team: 'MyTeam'
      });
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockWorkApi.getTeamIterations.mockRejectedValue('raw iter error');
      const response = await mockServer.invokeTool('work_list_team_iterations', {
        project: 'TBQPR',
        team: 'MyTeam'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw iter error');
    });
  });

  describe('work_assign_iterations', () => {
    it('should assign iterations to a team', async () => {
      mockWorkApi.postTeamIteration.mockResolvedValue({ id: 'iter-1', name: 'Sprint 1' });

      const response = await mockServer.invokeTool('work_assign_iterations', {
        project: 'TBQPR',
        team: 'MyTeam',
        iterations: [{ id: 'iter-guid-1' }, { id: 'iter-guid-2' }]
      });

      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWorkApi.postTeamIteration).toHaveBeenCalledTimes(2);
    });

    it('should return error on API failure', async () => {
      mockWorkApi.postTeamIteration.mockRejectedValue(new Error('Assign error'));
      const response = await mockServer.invokeTool('work_assign_iterations', {
        project: 'TBQPR',
        team: 'MyTeam',
        iterations: [{ id: 'iter-guid-1' }]
      });
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockWorkApi.postTeamIteration.mockRejectedValue('raw assign error');
      const response = await mockServer.invokeTool('work_assign_iterations', {
        project: 'TBQPR',
        team: 'MyTeam',
        iterations: [{ id: 'iter-guid-1' }]
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw assign error');
    });
  });

  describe('work_get_team_capacity', () => {
    it('should get team capacity for an iteration', async () => {
      const capacities = [{ teamMember: { displayName: 'John' }, activities: [{ name: 'Dev', capacityPerDay: 6 }] }];
      mockWorkApi.getCapacitiesWithIdentityRefAndTotals.mockResolvedValue(capacities);

      const response = await mockServer.invokeTool('work_get_team_capacity', {
        project: 'TBQPR',
        team: 'MyTeam',
        iterationId: 'iter-guid-1'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result[0].teamMember.displayName).toBe('John');
    });

    it('should return error on API failure', async () => {
      mockWorkApi.getCapacitiesWithIdentityRefAndTotals.mockRejectedValue(new Error('Capacity error'));
      const response = await mockServer.invokeTool('work_get_team_capacity', {
        project: 'TBQPR',
        team: 'MyTeam',
        iterationId: 'iter-guid-1'
      });
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockWorkApi.getCapacitiesWithIdentityRefAndTotals.mockRejectedValue('raw capacity error');
      const response = await mockServer.invokeTool('work_get_team_capacity', {
        project: 'TBQPR',
        team: 'MyTeam',
        iterationId: 'iter-guid-1'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw capacity error');
    });
  });

  describe('work_update_team_capacity', () => {
    it('should update team member capacity', async () => {
      const updated = { teamMember: { id: 'user-1' }, activities: [{ name: 'Dev', capacityPerDay: 8 }] };
      mockWorkApi.updateCapacityWithIdentityRef.mockResolvedValue(updated);

      const response = await mockServer.invokeTool('work_update_team_capacity', {
        project: 'TBQPR',
        team: 'MyTeam',
        iterationId: 'iter-guid-1',
        teamMemberId: 'user-guid-1',
        activities: [{ name: 'Dev', capacityPerDay: 8 }]
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.activities[0].capacityPerDay).toBe(8);
    });

    it('should update capacity with daysOff', async () => {
      mockWorkApi.updateCapacityWithIdentityRef.mockResolvedValue({});
      const response = await mockServer.invokeTool('work_update_team_capacity', {
        project: 'TBQPR',
        team: 'MyTeam',
        iterationId: 'iter-guid-1',
        teamMemberId: 'user-guid-1',
        activities: [{ name: 'Dev', capacityPerDay: 6 }],
        daysOff: [{ start: '2026-06-10', end: '2026-06-11' }]
      });
      expect(isValidToolResponse(response)).toBe(true);
      expect(mockWorkApi.updateCapacityWithIdentityRef).toHaveBeenCalledWith(
        expect.objectContaining({ daysOff: [{ start: '2026-06-10', end: '2026-06-11' }] }),
        expect.any(Object),
        'iter-guid-1',
        'user-guid-1'
      );
    });

    it('should return error on API failure', async () => {
      mockWorkApi.updateCapacityWithIdentityRef.mockRejectedValue(new Error('Update error'));
      const response = await mockServer.invokeTool('work_update_team_capacity', {
        project: 'TBQPR',
        team: 'MyTeam',
        iterationId: 'iter-guid-1',
        teamMemberId: 'user-guid-1',
        activities: [{ name: 'Dev', capacityPerDay: 8 }]
      });
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockWorkApi.updateCapacityWithIdentityRef.mockRejectedValue('raw update error');
      const response = await mockServer.invokeTool('work_update_team_capacity', {
        project: 'TBQPR',
        team: 'MyTeam',
        iterationId: 'iter-guid-1',
        teamMemberId: 'user-guid-1',
        activities: [{ name: 'Dev', capacityPerDay: 8 }]
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw update error');
    });
  });

  describe('work_get_team_settings', () => {
    it('should get team settings', async () => {
      const settings = { defaultIteration: { name: 'Sprint 1' }, backlogIteration: { name: 'Backlog' } };
      mockWorkApi.getTeamSettings.mockResolvedValue(settings);

      const response = await mockServer.invokeTool('work_get_team_settings', {
        project: 'TBQPR',
        team: 'MyTeam'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result.defaultIteration.name).toBe('Sprint 1');
    });

    it('should work without team parameter', async () => {
      mockWorkApi.getTeamSettings.mockResolvedValue({});
      const response = await mockServer.invokeTool('work_get_team_settings', { project: 'TBQPR' });
      expect(isValidToolResponse(response)).toBe(true);
    });

    it('should return error on API failure', async () => {
      mockWorkApi.getTeamSettings.mockRejectedValue(new Error('Settings error'));
      const response = await mockServer.invokeTool('work_get_team_settings', { project: 'TBQPR' });
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockWorkApi.getTeamSettings.mockRejectedValue('raw settings error');
      const response = await mockServer.invokeTool('work_get_team_settings', { project: 'TBQPR' });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw settings error');
    });
  });

  describe('work_get_iteration_capacities', () => {
    it('should get capacities for all teams in iteration', async () => {
      const teams = [{ name: 'Team A' }, { name: 'Team B' }];
      mockCoreApi.getTeams.mockResolvedValue(teams);
      mockWorkApi.getCapacitiesWithIdentityRefAndTotals.mockResolvedValue([]);

      const response = await mockServer.invokeTool('work_get_iteration_capacities', {
        project: 'TBQPR',
        iterationId: 'iter-guid-1'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(2);
    });

    it('should skip teams that throw errors', async () => {
      const teams = [{ name: 'Team A' }, { name: 'Team B' }];
      mockCoreApi.getTeams.mockResolvedValue(teams);
      mockWorkApi.getCapacitiesWithIdentityRefAndTotals
        .mockResolvedValueOnce([])
        .mockRejectedValueOnce(new Error('No access'));

      const response = await mockServer.invokeTool('work_get_iteration_capacities', {
        project: 'TBQPR',
        iterationId: 'iter-guid-1'
      });

      expect(isValidToolResponse(response)).toBe(true);
      const result = JSON.parse(response.content[0].text);
      expect(result).toHaveLength(1);
    });

    it('should return error when core API fails', async () => {
      mockCoreApi.getTeams.mockRejectedValue(new Error('Core API error'));
      const response = await mockServer.invokeTool('work_get_iteration_capacities', {
        project: 'TBQPR',
        iterationId: 'iter-guid-1'
      });
      expect(isValidErrorResponse(response)).toBe(true);
    });

    it('should handle non-Error thrown values', async () => {
      mockCoreApi.getTeams.mockRejectedValue('raw core error');
      const response = await mockServer.invokeTool('work_get_iteration_capacities', {
        project: 'TBQPR',
        iterationId: 'iter-guid-1'
      });
      expect(isValidErrorResponse(response)).toBe(true);
      expect(response.content[0].text).toBe('raw core error');
    });
  });
});
